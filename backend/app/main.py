from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from .detectors import heuristics, whois_check, ssl_check, dns_dyn_check, similarity, redirects

app = FastAPI()

class URLIn(BaseModel):
    url: HttpUrl

def run_heuristics(url):
    return {"blacklist": heuristics.in_blacklist(url),"patterns": heuristics.suspicious_pattern(url)}

CHECKS=[run_heuristics,whois_check.run,ssl_check.run,dns_dyn_check.run,similarity.run,redirects.run]

@app.post("/api/v1/analyze")
def analyze(item: URLIn):
    url=item.url
    results={}
    for check in CHECKS:
        results.update(check(url))
    malicious=any(v is True for v in results.values() if isinstance(v,bool))
    return {"url":url,"malicious":malicious,"details":results}
