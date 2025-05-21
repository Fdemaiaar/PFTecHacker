"""
Flag 'blacklist' – True se domínio OU URL estão no CSV do PhishTank
datasets/phishtank.csv  (formato padrão com cabeçalho)
"""

import csv, tldextract, pathlib, requests, time

DATA = pathlib.Path(__file__).resolve().parents[3] / "datasets" / "phishtank.csv"
PHISH_URLS: set[str] = set()
PHISH_DOMS: set[str] = set()

def _download():
    url = "https://data.phishtank.com/data/online-valid.csv"
    try:
        raw = requests.get(url, timeout=60).content
        DATA.write_bytes(raw)
        print("[phish] PhishTank atualizado", time.ctime())
    except Exception as e:
        print("[phish] download falhou:", e)

def _load():
    with DATA.open() as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            u = row["url"].strip().lower()
            d = tldextract.extract(u).registered_domain
            PHISH_URLS.add(u)
            PHISH_DOMS.add(d)

if not DATA.exists() or DATA.stat().st_size < 1000:
    _download()
_load()
print(f"[phish] URLs: {len(PHISH_URLS):,}  Domínios: {len(PHISH_DOMS):,}")

def run(url: str) -> dict[str, bool]:
    url_l = url.lower()
    dom   = tldextract.extract(url).registered_domain.lower()
    return {"blacklist": url_l in PHISH_URLS or dom in PHISH_DOMS}
