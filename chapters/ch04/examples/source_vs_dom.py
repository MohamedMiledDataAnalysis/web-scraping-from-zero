import requests
from bs4 import BeautifulSoup

for url in ["http://localhost:8000/quotes/",
            "http://localhost:8000/quotes/js/"]:
    soup = BeautifulSoup(requests.get(url, timeout=10).text, "html.parser")
    print(url, "->", len(soup.select("div.quote")), "quotes in the source")
