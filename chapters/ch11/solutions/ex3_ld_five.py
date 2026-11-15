import json
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

session = requests.Session()
base = "http://localhost:8000/library/"
soup = BeautifulSoup(session.get(base, timeout=10).text, "html.parser")
for card in soup.select("article.book-card")[:5]:
    url = urljoin(base, card.select_one("h3 a")["href"])
    page = BeautifulSoup(session.get(url, timeout=10).text, "html.parser")
    ld = json.loads(page.find("script", type="application/ld+json").string)
    status = ld["offers"]["availability"].rsplit("/", 1)[-1]
    print(ld["name"], ld["offers"]["price"], status)
