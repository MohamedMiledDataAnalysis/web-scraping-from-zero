import requests
from bs4 import BeautifulSoup

RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def parse_card(card):
    """One book card of the library -> one dictionary."""
    link = card.select_one("h3 a")
    rating = card.select_one("p.star-rating")
    price = card.select_one("p.price")
    return {
        "id": int(card["data-id"]),
        "title": link["title"] if link else None,
        "url": link["href"] if link else None,
        "author": card.select_one("p.author").text.removeprefix("by ")
        if card.select_one("p.author") else None,
        "rating": RATINGS.get(rating["class"][1]) if rating else None,
        "price": float(price.text.replace("£", "")) if price else None,
        "in_stock": card.select_one("p.in-stock") is not None,
    }


html = requests.get("http://localhost:8000/library/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
books = [parse_card(c) for c in soup.select("article.book-card")]
print(len(books))
for b in books[:2]:
    print(b)
