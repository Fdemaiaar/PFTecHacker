# scripts/sanitize_phishtank.py
import pandas as pd, urllib.parse as up, pathlib, re

SRC = pathlib.Path("datasets/phishtank.csv")          # original bruto
DST = pathlib.Path("datasets/phishtank_clean.csv")    # destino limpo

aws_key_rgx = re.compile(r"AKIA[0-9A-Z]{16}")         # chave AWS

def sanitize(u: str) -> str:
    # remove query e fragmento
    p = up.urlparse(u)
    clean = f"{p.scheme}://{p.netloc}{p.path}"
    # se ainda contiver possível chave, troca por <redacted>
    return aws_key_rgx.sub("<redacted>", clean)

df = pd.read_csv(SRC, usecols=["url"])
df["url"] = df["url"].astype(str).map(sanitize)
df.drop_duplicates().to_csv(DST, index=False)
print("Gerado", DST, "com", len(df), "linhas")
