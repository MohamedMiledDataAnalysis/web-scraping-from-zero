import hashlib
from pathlib import Path

import requests

CACHE = Path("output/cache")
CACHE.mkdir(parents=True, exist_ok=True)


def get_html(url):
    """Return the page's HTML, from the cache if it was downloaded before."""
    name = hashlib.sha1(url.encode()).hexdigest()[:16] + ".html"
    path = CACHE / name
    if path.exists():
        print("from cache:", url)
        return path.read_text(encoding="utf-8")
    print("downloading:", url)
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    path.write_text(r.text, encoding="utf-8")
    return r.text


for _ in range(2):
    html = get_html("http://localhost:8000/library/page-3.html")
print(len(html), "characters")
