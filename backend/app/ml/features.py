import tldextract, datetime as dt
from urllib.parse import urlparse
def vector(url, meta):
 r=[]
 p=urlparse(url)
 r+=[len(url), p.netloc.count('.'), int(any(c.isdigit() for c in p.netloc)), int('-' in p.netloc)]
 r+=[meta.get('age_days', 0), int(meta.get('ssl_expired', 0)), int(meta.get('dynamic_dns', 0))]
 r+=[int(meta.get('brand_similar', 0)), meta.get('hops', 0)]
 return r
