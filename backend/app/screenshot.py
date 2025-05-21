from hashlib import sha1
from pathlib import Path
from playwright.sync_api import sync_playwright

media = Path("media/shots")
media.mkdir(parents=True, exist_ok=True)

def capture(url: str) -> str | None:
    fn = media / f"{sha1(url.encode()).hexdigest()[:12]}.png"
    if fn.exists():
        return str(fn)

    try:
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True)
            page = b.new_page()
            page.goto(url, timeout=8_000, wait_until="load")
            page.screenshot(path=fn, full_page=True)
            b.close()
        return str(fn) if fn.exists() else None
    except Exception:
        return None
