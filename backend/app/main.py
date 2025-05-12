from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel,HttpUrl
from .detectors import heuristics,whois_check,ssl_check,dns_dyn_check,similarity,redirects
from .ml import risk
from .screenshot import capture
app=FastAPI()
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_methods=['*'],allow_headers=['*'])
class URLIn(BaseModel):url:HttpUrl
def _legacy(url):
 return {"blacklist":heuristics.in_blacklist(url),"patterns":heuristics.suspicious_pattern(url)}|whois_check.run(url)|ssl_check.run(url)|dns_dyn_check.run(url)|similarity.run(url)|redirects.run(url)
@app.post('/api/v2/score')
def score(inp:URLIn):
 url=str(inp.url)
 details=_legacy(url)
 score=risk(url,details)
 shot=capture(url)
 return {"url":url,"score":score,"details":details,"screenshot":shot}
app.mount('/',StaticFiles(directory='web',html=True),name='static')
