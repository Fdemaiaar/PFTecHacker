from hashlib import md5,sha1
from pathlib import Path
from playwright.sync_api import sync_playwright
media=Path('media/shots');media.mkdir(parents=True,exist_ok=True)
def capture(url):
 fn=media/f'{sha1(url.encode()).hexdigest()[:12]}.png'
 if fn.exists():return str(fn)
 with sync_playwright() as p:
  b=p.chromium.launch()
  page=b.new_page();page.goto(url,timeout=8000)
  page.screenshot(path=fn,full_page=True)
  b.close()
 return str(fn)
