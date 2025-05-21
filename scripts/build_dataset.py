import pathlib, sys, io, random, time, requests, pandas as pd
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from backend.app.detectors import dns_dyn_check, similarity, redirects

# ---------- util ----------
def download(url, retries=3, t=90):
    for _ in range(retries):
        try:
            r = requests.get(url, timeout=t); r.raise_for_status(); return r.content
        except Exception as e:
            print("download erro:", e); time.sleep(5)
    raise RuntimeError(f"Falha ao baixar {url}")

def safe(det, url):
    try:   return det.run(url) if hasattr(det, "run") else det(url)
    except: return {}

# ---------- baixar ----------
print("Baixando PhishTank…")
df_phish = pd.read_csv(io.BytesIO(download("https://data.phishtank.com/data/online-valid.csv")),
                       usecols=["url"]).head(15000)
df_phish["label"] = 1

print("Lendo Tranco Top-1M local…")
df_legit = pd.read_csv("datasets/tranco_top1m.csv", header=None, names=["rank", "domain"])
df_legit = df_legit.dropna(subset=["domain"]).head(15000)
df_legit["url"] = "https://" + df_legit["domain"].astype(str).str.strip()
df_legit = df_legit[["url"]]; df_legit["label"] = 0

# ---------- mistura ----------
df = pd.concat([df_phish, df_legit], ignore_index=True)\
       .sample(frac=1, random_state=42).reset_index(drop=True)

meta_cols = ["dynamic_dns", "brand_similar", "hops"]
for c in meta_cols: df[c] = 0

# ---------- features ----------
print("Gerando metadados (~30k URLs; 500 ≈ 10 min)…")
for i, url in enumerate(df.url):
    meta = {}
    meta |= safe(dns_dyn_check, url)
    meta |= safe(similarity, url)
    meta |= safe(redirects, url)            # mantém redirects; altera se quiser +rápido
    for k in meta_cols: df.at[i, k] = int(bool(meta.get(k, 0)))
    if i and i % 500 == 0: print(i, "urls processadas")

# ---------- salvar ----------
datasets = ROOT / "datasets"; datasets.mkdir(exist_ok=True)
out = datasets / "train.csv"; df.to_csv(out, index=False)
print("Dataset salvo em", out, "linhas:", len(df))
