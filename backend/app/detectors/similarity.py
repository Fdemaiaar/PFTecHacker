import Levenshtein,tldextract,re
BRANDS=["paypal","facebook","microsoft","google","apple","netflix"]
TH=4
def _clean(s):return re.sub(r'[^a-z]','',s.lower())
def run(url):
    dom=_clean(tldextract.extract(url).domain)
    closest=min(BRANDS,key=lambda b:Levenshtein.distance(dom,b))
    dist=Levenshtein.distance(dom,closest)
    return {"brand_similar": dist<=TH,"closest_brand":closest if dist<=TH else None}
