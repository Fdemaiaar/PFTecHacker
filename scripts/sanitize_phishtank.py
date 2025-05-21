#!/usr/bin/env python
"""
Converte datasets/phishtank.csv  →  datasets/phishtank_clean.csv
• Mantém apenas a coluna 'url'
• Remove query-string e fragmento
• Redact (substitui) possíveis chaves AWS detectadas
"""

import re
import urllib.parse as up
from pathlib import Path

import pandas as pd

SRC = Path("datasets/phishtank.csv")          # original bruto BAIXADO
DST = Path("datasets/phishtank_clean.csv")    # destino limpo

AWS_RGX = re.compile(r"AKIA[0-9A-Z]{16}")     # padrão Access-Key

def sanitize(raw_url: str) -> str:
    p = up.urlparse(raw_url)
    # host + path sem query/fragmento
    clean = f"{p.scheme}://{p.netloc}{p.path}"
    # remove eventual chave AWS
    return AWS_RGX.sub("<redacted>", clean)

def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"[erro] Arquivo {SRC} não encontrado")

    df = pd.read_csv(SRC, usecols=["url"])
    df["url"] = df["url"].astype(str).map(sanitize)
    df.drop_duplicates().to_csv(DST, index=False)
    print(f"[ok] Gerado {DST} com {len(df)} linhas")

if __name__ == "__main__":
    main()
