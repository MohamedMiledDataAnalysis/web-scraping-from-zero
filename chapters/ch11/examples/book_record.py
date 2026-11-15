import json
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def parse_book_page(url, html):
    soup = BeautifulSoup(html, "html.parser")
    ld = {}
    script = soup.find("script", type="application/ld+json")
    if script:
        ld = json.loads(script.string)
    info = {r.th.text: r.td.text for r in soup.select("table.info tr")}
    stock_text = info.get("Availability", "")
    return {
        "url": url,
        "title": ld.get("name") or soup.h1.text,
        "author": ld.get("author", {}).get("name"),
        "category": ld.get("genre") or info.get("Category"),
        "price": (
            float(ld["offers"]["price"]) if "offers" in ld else None
        ),
        "rating": ld.get("aggregateRating", {}).get("ratingValue"),
        "stock": (
            int(stock_text.split("(")[1].split()[0])
            if "(" in stock_text
            else None
        ),
        "upc": info.get("UPC"),
        "pages": ld.get("numberOfPages"),
        "year": (
            int(ld["datePublished"]) if "datePublished" in ld else None
        ),
        "description": soup.select_one("#description p").text,
    }


base = "http://localhost:8000/library/"
url = urljoin(base, "book/the-broken-forest-1.html")
record = parse_book_page(url, requests.get(url, timeout=10).text)
for key, value in record.items():
    print(f"{key:<12} {value}")
