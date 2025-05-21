"""
popular_domain  ➜  True  se o domínio registrado (e somente ele) aparecer no
                   Tranco Top-1 M **e** o sub-domínio for vazio ou “www”.
                   False caso contrário.
"""

from pathlib import Path
import csv
import tldextract

# ────────────────────────────────────────────────────────────────────
CSV_PATH = Path(__file__).resolve().parents[3] / "datasets" / "tranco_top1m.csv"
TOP: set[str] = set()

with CSV_PATH.open() as fh:
    for rank, domain in csv.reader(fh):
        TOP.add(domain.strip().lower())

# subdomínios genéricos que ainda consideramos “populares”
GENERIC_SUBS = {"", "www"}

# ────────────────────────────────────────────────────────────────────
def run(url: str) -> dict[str, bool]:
    """
    Retorna {"popular_domain": bool}.
    Ex.:  google.com        → True
          www.google.com    → True
          mail.google.com   → False
          foo.firebaseapp.com → False (mesmo que firebaseapp.com esteja no Top-1 M)
    """
    ext = tldextract.extract(url)
    base = ext.registered_domain.lower()
    sub  = ext.subdomain.lower()
    popular = base in TOP and sub in GENERIC_SUBS
    return {"popular_domain": popular}
