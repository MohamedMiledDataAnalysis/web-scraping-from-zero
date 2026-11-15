import json

from bs4 import BeautifulSoup


def parse_book_page(url, html):
    """The detail page of one library book -> one dictionary (Chapter 11)."""
    soup = BeautifulSoup(html, "html.parser")
    script = soup.find("script", type="application/ld+json")
    ld = json.loads(script.string) if script else {}
    info = {r.th.text: r.td.text for r in soup.select("table.info tr")}
    stock_text = info.get("Availability", "")
    return {
        "url": url,
        "title": ld.get("name") or soup.h1.text,
        "author": ld.get("author", {}).get("name"),
        "category": ld.get("genre") or info.get("Category"),
        "price": float(ld["offers"]["price"]) if "offers" in ld else None,
        "rating": ld.get("aggregateRating", {}).get("ratingValue"),
        "stock": int(stock_text.split("(")[1].split()[0]) if "(" in stock_text else None,
        "pages": ld.get("numberOfPages"),
        "year": int(ld["datePublished"]) if "datePublished" in ld else None,
    }
