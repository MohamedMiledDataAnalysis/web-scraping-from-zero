import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

session = requests.Session()
visited = set()
authors = []

url = "http://localhost:8000/quotes/"
while url:
    soup = BeautifulSoup(
        session.get(url, timeout=10).text, "html.parser"
    )
    visited.add(url)
    for link in soup.select('span.by a[href*="/author/"]'):
        author_url = urljoin(url, link["href"])
        if author_url in visited:
            continue
        visited.add(author_url)
        time.sleep(0.2)
        page = BeautifulSoup(
            session.get(author_url, timeout=10).text, "html.parser"
        )
        authors.append(
            {
                "name": page.select_one("h1.author-title").text,
                "born": page.select_one("span.author-born-date").text,
            }
        )
    nxt = soup.select_one("li.next a")
    url = urljoin(url, nxt["href"]) if nxt else None
    if url in visited:
        break
    time.sleep(0.2)

print(len(visited), "pages visited for 40 quotes")
for a in sorted(authors, key=lambda a: a["born"]):
    print(a["born"], a["name"])
