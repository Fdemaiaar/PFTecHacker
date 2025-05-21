from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl, field_validator

from backend.app.detectors import (
    top1m_known,
    phish_blacklist,
    whois_check,
    ssl_check,
    dns_dyn_check,
    similarity,
    redirects,
    heuristics,
)

from backend.app.ml import risk
from backend.app.screenshot import capture

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# ----------------------------------------------------------------------
class URLIn(BaseModel):
    url: HttpUrl

    # adiciona http:// se faltar esquema
    @field_validator("url", mode="before")
    @classmethod
    def ensure_scheme(cls, v: str):
        v = str(v)
        if not v.startswith(("http://", "https://")):
            v = "http://" + v
        return v


# ----------------------------------------------------------------------
def legacy_flags(url: str) -> dict:
    flags = {
        "popular_domain": top1m_known.run(url)["popular_domain"],
        "blacklist":     phish_blacklist.run(url)["blacklist"],
        "patterns":      heuristics.suspicious_pattern(url),
    }
    flags.update(whois_check.run(url))
    flags.update(ssl_check.run(url))
    flags.update(dns_dyn_check.run(url))
    flags.update(similarity.run(url))
    flags.update(redirects.run(url))
    return flags


@app.post("/api/v2/score")
def score(inp: URLIn):
    url = str(inp.url)
    details = legacy_flags(url)
    score_val = risk(url, details)
    shot = capture(url)
    return {
        "url": url,
        "score": score_val,
        "details": details,
        "screenshot": f"/{shot}" if shot else None,
    }



# ----------------------------------------------------------------------
# arquivos estáticos
app.mount("/media", StaticFiles(directory="media"), name="media")
app.mount("/",      StaticFiles(directory="web",   html=True), name="static")

