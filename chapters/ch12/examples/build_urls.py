import re
import time

import requests
from bs4 import BeautifulSoup

session = requests.Session()
first = BeautifulSoup(
    session.get("http://localhost:8000/library/", timeout=10).text,
    "html.parser",
)
count_text = first.select_one("p.result-count").text
total_pages = int(re.search(r"of (\d+)", count_text).group(1))
print(count_text, "->", total_pages, "pages")

prices = []
for page in range(1, total_pages + 1):
    url = f"http://localhost:8000/library/page-{page}.html"
    soup = BeautifulSoup(
        session.get(url, timeout=10).text, "html.parser"
    )
    prices += [float(p.text[1:]) for p in soup.select("p.price")]
    time.sleep(0.2)
print(
    len(prices),
    "prices, average £" + f"{sum(prices) / len(prices):.2f}",
)
