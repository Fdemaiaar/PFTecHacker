import httpx,urllib.parse as up
def run(url):
    try:
        r=httpx.get(url,follow_redirects=True,timeout=5)
        hops=len(r.history)
    except Exception:
        return {"redirect_suspicious":True,"hops":None}
    return {"redirect_suspicious":hops>1,"hops":hops}
