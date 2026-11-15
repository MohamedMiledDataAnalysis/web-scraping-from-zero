from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

page = "http://localhost:8000/files/"
soup = BeautifulSoup(requests.get(page, timeout=10).text, "html.parser")
selector = ('a[href$=".csv"], a[href$=".xlsx"], '
            'a[href$=".pdf"], a[href$=".txt"]')
for a in soup.select(selector):
    print(urljoin(page, a["href"]))
