import json
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

session = requests.Session()
base = "http://localhost:8000/library/"
soup = BeautifulSoup(session.get(base, timeout=10).text, "html.parser")
checked = differences = 0
for card in soup.select("article.book-card"):
    visible = float(card.select_one("p.price").text.replace("£", ""))
    url = urljoin(base, card.select_one("h3 a")["href"])
    page = BeautifulSoup(session.get(url, timeout=10).text, "html.parser")
    ld = json.loads(page.find("script", type="application/ld+json").string)
    checked += 1
    if abs(visible - float(ld["offers"]["price"])) > 0.001:
        differences += 1
        print("Difference:", url)
print(checked, "books checked,", differences, "differences")
