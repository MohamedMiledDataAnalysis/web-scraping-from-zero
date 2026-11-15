import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/library/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
cheapest = min(soup.find_all("p", class_="price"),
               key=lambda p: float(p.text.replace("£", "")))
card = cheapest.find_parent("article")
print(cheapest.text, card.h3.a["title"], card["data-id"])
