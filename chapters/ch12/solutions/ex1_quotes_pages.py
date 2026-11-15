import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

session = requests.Session()
url, pages, quotes = "http://localhost:8000/quotes/", 0, 0
while url:
    soup = BeautifulSoup(session.get(url, timeout=10).text, "html.parser")
    pages += 1
    quotes += len(soup.select("div.quote"))
    nxt = soup.select_one("li.next a")
    url = urljoin(url, nxt["href"]) if nxt else None
    time.sleep(0.2)
print(pages, "pages,", quotes, "quotes")
