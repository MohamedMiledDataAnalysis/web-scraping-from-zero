"""Method 1: requests + BeautifulSoup on the 50 list pages."""
import json
import sys
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
from bs4 import BeautifulSoup

sys.path.insert(0, ".")
from toolkit.polite import PoliteClient  # noqa: E402

RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
OUT = Path("output/ch23")
OUT.mkdir(parents=True, exist_ok=True)
client = PoliteClient("LearningScraper/1.0 (+mailto:reader@example.com)", delay=0.2)

rows, requests_sent = [], 0
url = "http://localhost:8000/library/"
while url:
    soup = BeautifulSoup(client.get(url).text, "html.parser")
    requests_sent += 1
    for card in soup.select("article.book-card"):
        link = card.select_one("h3 a")
        rows.append({
            "url": urljoin(url, link["href"]),
            "title": link["title"],
            "author": card.select_one("p.author").text.removeprefix("by "),
            "price": float(card.select_one("p.price").text[1:]),
            "rating": RATINGS[card.select_one("p.star-rating")["class"][1]],
            "in_stock": card.select_one("p.in-stock") is not None,
        })
    nxt = soup.select_one("ul.pager li.next a")
    url = urljoin(url, nxt["href"]) if nxt else None

books = pd.DataFrame(rows)
books.to_csv(OUT / "m1_list_pages.csv", index=False)
(OUT / "m1_meta.json").write_text(json.dumps({"requests": requests_sent}))
print(len(books), "books,", requests_sent, "requests,", len(books.columns), "columns")
