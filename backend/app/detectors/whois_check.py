"""Idade do domínio (`whois_age_days`) e flag `young_domain`."""

import datetime as dt
from typing import Dict, Union, Optional

import tldextract
import whois

THRESHOLD = 180  # dias para considerar “jovem”


def _creation_date(rec: whois.whois) -> Optional[dt.datetime]:
    """
    Extrai a creation_date do objeto whois.
    Pode vir como datetime, lista de datetimes ou None.
    """
    cd = rec.creation_date
    if isinstance(cd, list):
        cd = cd[0]  # pega o primeiro valor
    return cd if isinstance(cd, dt.datetime) else None


def run(url: str) -> Dict[str, Union[int, bool, None]]:
    """
    Retorna:
        whois_age_days : int | None   (None quando data indisponível)
        young_domain   : bool         (True se idade < THRESHOLD)
    """
    domain = tldextract.extract(url).registered_domain
    try:
        w = whois.whois(domain)
        cd = _creation_date(w)
    except Exception:
        cd = None

    if cd is None:
        # Sem data → não marcamos como jovem para não gerar falso-positivo
        return {"whois_age_days": None, "young_domain": False}

    age = (dt.datetime.utcnow() - cd).days
    return {"whois_age_days": age, "young_domain": age < THRESHOLD}
