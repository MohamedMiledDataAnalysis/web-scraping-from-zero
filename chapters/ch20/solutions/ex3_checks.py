import sys

import pandas as pd
from bs4 import BeautifulSoup

sys.path.insert(0, ".")
sys.path.insert(0, "chapters/ch20/examples")
from checks import check_books  # noqa: E402
from toolkit.polite import PoliteClient  # noqa: E402

client = PoliteClient("LearningScraper/1.0", delay=0.2)


def scrape(price_selector):
    rows = []
    for page in range(1, 6):
        html = client.get(f"http://localhost:8000/library/page-{page}.html").text
        for card in BeautifulSoup(html, "html.parser").select("article.book-card"):
            price = card.select_one(price_selector)
            rows.append({"title": card.select_one("h3 a")["title"],
                         "price": float(price.text[1:]) if price else None})
    return pd.DataFrame(rows)


print(check_books(scrape("p.price"), expected_rows=100))
print(check_books(scrape("p.cost"), expected_rows=100))
