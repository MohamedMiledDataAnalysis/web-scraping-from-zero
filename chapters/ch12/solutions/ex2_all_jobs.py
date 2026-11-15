import time
from collections import Counter
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

session = requests.Session()
url, cities = "http://localhost:8000/jobs/", []
while url:
    soup = BeautifulSoup(
        session.get(url, timeout=10).text, "html.parser"
    )
    cities += [
        li.select_one("p.location").text for li in soup.select("li.job")
    ]
    nxt = soup.select_one("ul.pager li.next a")
    url = urljoin(url, nxt["href"]) if nxt else None
    time.sleep(0.2)
print(len(cities), "jobs")
print(Counter(cities).most_common(3))
