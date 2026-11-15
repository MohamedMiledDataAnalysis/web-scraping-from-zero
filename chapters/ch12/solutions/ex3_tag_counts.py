import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

session = requests.Session()
base = "http://localhost:8000/quotes/"
home = BeautifulSoup(session.get(base, timeout=10).text, "html.parser")
tag_urls = {a.text: urljoin(base, a["href"]) for a in home.select("aside.tag-box a")}

counts = {}
for tag, url in tag_urls.items():
    n = 0
    while url:
        time.sleep(0.2)
        soup = BeautifulSoup(session.get(url, timeout=10).text, "html.parser")
        n += len(soup.select("div.quote"))
        nxt = soup.select_one("li.next a")
        url = urljoin(url, nxt["href"]) if nxt else None
    counts[tag] = n

for tag, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:5]:
    print(tag, n)
