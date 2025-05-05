import re, requests, csv, pathlib, datetime, urllib.parse as up

BL_PATH = pathlib.Path("data/phishtank.csv")
SUBDOMAIN_THRESH = 3          # “excessivo”
DEF_CHARS = r"[^A-Za-z0-9\-./:]"

def load_blacklist():
    if BL_PATH.exists():               # CSV: url,status
        with BL_PATH.open() as f:
            return {row[0] for row in csv.reader(f) if row[1]=="phish"}
    return set()

BLACKLIST = load_blacklist()

def in_blacklist(url):
    return url in BLACKLIST

def suspicious_pattern(url):
    host = up.urlparse(url).netloc.lower()
    if sum(1 for c in host if c.isdigit()) > 3:        # números excessivos
        return True
    if host.count('.') - 1 >= SUBDOMAIN_THRESH:        # subdomínios
        return True
    if re.search(DEF_CHARS, host):
        return True
    return False
