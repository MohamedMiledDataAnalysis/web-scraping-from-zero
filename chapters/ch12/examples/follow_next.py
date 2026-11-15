import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

DELAY = 0.2  # the Practice Ground's terms
session = requests.Session()
session.headers["User-Agent"] = (
    "LearningScraper/1.0 (+mailto:reader@example.com)"
)

url = "http://localhost:8000/library/"
titles, pages = [], 0
while url:
    response = session.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    titles += [
        a["title"] for a in soup.select("article.book-card h3 a")
    ]
    pages += 1
    next_link = soup.select_one("ul.pager li.next a")
    url = urljoin(url, next_link["href"]) if next_link else None
    time.sleep(DELAY)

print(pages, "pages,", len(titles), "books")
print("Last book:", titles[-1])
