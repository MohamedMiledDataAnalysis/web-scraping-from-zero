import json

import requests
from bs4 import BeautifulSoup

url = "http://localhost:8000/library/book/salt-kingdom-2.html"
soup = BeautifulSoup(requests.get(url, timeout=10).text, "html.parser")
script = soup.find("script", type="application/ld+json")
data = json.loads(script.string)
print(data["@type"], "|", data["name"], "|", data["author"]["name"])
print(data["offers"]["price"], data["offers"]["priceCurrency"])
print(data["offers"]["availability"].rsplit("/", 1)[-1])
print(data["aggregateRating"]["ratingValue"], data["numberOfPages"])
