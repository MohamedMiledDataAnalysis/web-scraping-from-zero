import time
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

from book_parser import parse_book_page

DELAY = 0.2
session = requests.Session()
session.headers["User-Agent"] = (
    "LearningScraper/1.0 (+mailto:reader@example.com)"
)


def get_html(url):
    time.sleep(DELAY)
    response = session.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def get_soup(url):
    return BeautifulSoup(get_html(url), "html.parser")


# Level 1: the list pages of the category -> detail addresses
detail_urls = []
url = "http://localhost:8000/library/category/history/"
while url:
    soup = get_soup(url)
    for a in soup.select("article.book-card h3 a"):
        detail_urls.append(urljoin(url, a["href"]))
    nxt = soup.select_one("ul.pager li.next a")
    url = urljoin(url, nxt["href"]) if nxt else None
print(len(detail_urls), "books in History")

# Level 2: every detail page -> one record
records = []
for i, detail in enumerate(detail_urls, start=1):
    records.append(parse_book_page(detail, get_html(detail)))
    if i % 20 == 0:
        print(i, "detail pages done")

books = pd.DataFrame(records)
Path("output/ch12").mkdir(parents=True, exist_ok=True)
books.to_csv("output/ch12/history_books.csv", index=False)
print(books[["title", "price", "stock"]].head(3).to_string())
print("Total stock:", books["stock"].sum())
