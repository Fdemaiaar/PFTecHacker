"""
Heurísticas estáticas rápidas
─────────────────────────────
• in_blacklist(url)      → host da URL consta no CSV limpo do PhishTank
• suspicious_pattern(url)→ indícios léxicos suspeitos no domínio
"""

from __future__ import annotations

import pathlib
import re
import urllib.parse as up
from typing import Set

import pandas as pd

# ────────────────────────────────────────────────────────────────────
# CONSTANTES / CONFIG

PHISH_PATH = pathlib.Path("datasets/phishtank_clean.csv")  # CSV já sanitizado
SUBDOMAIN_THRESH = 3                                       # “excessivo”
DEF_CHARS = r"[^A-Za-z0-9\-./:]"                           # caracteres estranhos

# ────────────────────────────────────────────────────────────────────
# BLACKLIST

def _load_blacklist() -> Set[str]:
    """
    Carrega todos os **hosts** presentes no CSV limpo (uma coluna 'url').
    O host (netloc) é transformado para lower-case e guardado em um set.
    """
    if not PHISH_PATH.exists():
        return set()

    print("[heuristics] carregando blacklist do PhishTank -", PHISH_PATH)
    df = pd.read_csv(PHISH_PATH, usecols=["url"])
    hosts = {
        up.urlparse(u).netloc.lower().lstrip("www.")
        for u in df["url"].astype(str)
        if isinstance(u, str)
    }
    return hosts


BLACKLIST = _load_blacklist()


def in_blacklist(url: str) -> bool:
    """Retorna **True** se o host da URL existir no conjunto PhishTank."""
    host = up.urlparse(url).netloc.lower().lstrip("www.")
    return host in BLACKLIST


# ────────────────────────────────────────────────────────────────────
# PADRÕES SUSPEITOS

def suspicious_pattern(url: str) -> bool:
    """
    Detecta indícios léxicos simples:
      • Muitos dígitos no domínio
      • Número de subdomínios > SUBDOMAIN_THRESH
      • Caracteres fora do conjunto seguro
    """
    host = up.urlparse(url).netloc.lower()

    # Muitos dígitos no nome
    if sum(ch.isdigit() for ch in host) > 3:
        return True

    # Subdomínios demais  (ex.: x.y.z.a.b.com → 4 pontos além do TLD)
    if host.count(".") - 1 >= SUBDOMAIN_THRESH:
        return True

    # Caracteres incomuns
    if re.search(DEF_CHARS, host):
        return True

    return False
