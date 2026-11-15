from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

session = requests.Session()
rows = []
for page in [1, 2, 1, 2]:
    url = f"http://localhost:8000/library/page-{page}.html"
    soup = BeautifulSoup(
        session.get(url, timeout=10).text, "html.parser"
    )
    for card in soup.select("article.book-card"):
        rows.append(
            {
                "id": int(card["data-id"]),
                "title": card.select_one("h3 a")["title"],
                "rating": card.select_one("p.star-rating")["class"][1],
                "price": float(card.select_one("p.price").text[1:]),
            }
        )
books = pd.DataFrame(rows)
clean = books.drop_duplicates(subset="id")
print(len(books), "rows,", len(clean), "distinct books")
Path("output/ch13").mkdir(parents=True, exist_ok=True)
clean.to_csv("output/ch13/books_p1_p2.csv", index=False)
