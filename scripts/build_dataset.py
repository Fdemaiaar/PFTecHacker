import pathlib, sys, io, random, time, requests, pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from backend.app.detectors import whois_check, ssl_check, dns_dyn_check, similarity, redirects

def download(url, retries=3, timeout=90):
    for _ in range(retries):
        try:
            r = requests.get(url, timeout=timeout)
            r.raise_for_status()
            return r.content
        except Exception as e:
            print("download erro:", e)
            time.sleep(5)
    raise RuntimeError(f"Falha ao baixar {url}")

print("Baixando PhishTank…")
phish_raw = download("https://data.phishtank.com/data/online-valid.csv")
df_phish = pd.read_csv(io.BytesIO(phish_raw), usecols=["url"])
df_phish["label"] = 1

print("Lendo Tranco Top‑1M local…")
df_legit = pd.read_csv("datasets/tranco_top1m.csv", header=None, names=["rank", "domain"])
df_legit = df_legit.dropna(subset=["domain"]).head(10000)
df_legit["domain"] = df_legit["domain"].astype(str).str.strip()
df_legit["url"] = "https://" + df_legit["domain"]
df_legit = df_legit[["url"]]
df_legit["label"] = 0

df = pd.concat([df_phish, df_legit], ignore_index=True)
random.seed(42)
df = df.sample(frac=1).reset_index(drop=True)

meta_cols = ["age_days", "ssl_expired", "dynamic_dns", "brand_similar", "hops"]
for c in meta_cols:
    df[c] = 0

def safe(det, url):
    try:
        return det(url)
    except Exception:
        return {}

print("Gerando metadados (pode demorar)…")
for i, row in df.iterrows():
    url = row.url
    meta = {}
    meta |= safe(whois_check.run, url)
    meta |= safe(ssl_check.run, url)
    meta |= safe(dns_dyn_check.run, url)
    meta |= safe(similarity.run, url)
    meta |= safe(redirects.run, url)
    for k in meta_cols:
        df.at[i, k] = meta.get(k, 0)
    if i % 500 == 0:
        print(i, "urls processadas")

datasets = ROOT / "datasets"
datasets.mkdir(exist_ok=True, parents=True)
out = datasets / "train.csv"
df.to_csv(out, index=False)
print("Salvo em", out, "linhas:", len(df))
