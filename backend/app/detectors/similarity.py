import Levenshtein,tldextract
BRANDS=["paypal","facebook","microsoft","google","apple","netflix"]
TH=3
def run(url):
    dom=tldextract.extract(url).domain
    closest=min(BRANDS,key=lambda b:Levenshtein.distance(dom,b))
    dist=Levenshtein.distance(dom,closest)
    return {"brand_similar": dist<=TH,"closest_brand":closest if dist<=TH else None}
