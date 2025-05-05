from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl
from .detectors import (
    heuristics,
    whois_check,
    ssl_check,
    dns_dyn_check,
    similarity,
    redirects,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLIn(BaseModel):
    url: HttpUrl

def run_heuristics(url: str) -> dict:
    return {
        "blacklist": heuristics.in_blacklist(url),
        "patterns": heuristics.suspicious_pattern(url),
    }

CHECKS = [
    run_heuristics,
    whois_check.run,
    ssl_check.run,
    dns_dyn_check.run,
    similarity.run,
    redirects.run,
]

@app.post("/api/v1/analyze")
def analyze(item: URLIn) -> dict:
    url = str(item.url)              # <-- converte para string simples
    results = {}
    for check in CHECKS:
        results.update(check(url))
    malicious = any(
        value is True for value in results.values() if isinstance(value, bool)
    )
    return {"url": url, "malicious": malicious, "details": results}

app.mount("/", StaticFiles(directory="web", html=True), name="static")
