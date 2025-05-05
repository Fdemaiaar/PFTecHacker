from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from .detectors.heuristics import in_blacklist, suspicious_pattern

app = FastAPI()

class URLIn(BaseModel):
    url: HttpUrl

@app.post("/api/v1/analyze")
def analyze(item: URLIn):
    url = item.url
    flags = {
        "blacklist": in_blacklist(url),
        "patterns": suspicious_pattern(url)
    }
    malicious = any(flags.values())
    return {"url": url, "malicious": malicious, "flags": flags}
