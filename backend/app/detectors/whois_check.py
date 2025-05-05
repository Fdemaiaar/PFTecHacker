import whois, datetime as dt
def run(url):
    try:
        w = whois.whois(url)
        age_days = (dt.datetime.now() - w.creation_date).days
    except Exception:
        return {"whois_age_days": None, "young_domain": True}
    return {"whois_age_days": age_days, "young_domain": age_days < 90}
