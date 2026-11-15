import sys
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, "chapters/ch12/examples")
from book_parser import parse_book_page  # noqa: E402

session = requests.Session()
url, records = "http://localhost:8000/library/category/poetry/", []
while url:
    soup = BeautifulSoup(
        session.get(url, timeout=10).text, "html.parser"
    )
    for a in soup.select("article.book-card h3 a"):
        detail = urljoin(url, a["href"])
        time.sleep(0.2)
        records.append(
            parse_book_page(
                detail, session.get(detail, timeout=10).text
            )
        )
    nxt = soup.select_one("li.next a")
    url = urljoin(url, nxt["href"]) if nxt else None

longest = max(records, key=lambda r: r["pages"])
print(longest["title"], longest["pages"])
print(round(sum(r["rating"] for r in records) / len(records), 2))
