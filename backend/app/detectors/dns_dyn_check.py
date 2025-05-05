import tldextract
DYN_PROVIDERS={"no-ip","duckdns","dyndns"}
def run(url):
    ext=tldextract.extract(url)
    dyn=ext.domain in DYN_PROVIDERS
    return {"dynamic_dns": dyn}
