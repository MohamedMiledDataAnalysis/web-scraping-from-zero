import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/library/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
card = soup.find("article", class_="book-card")
link = card.h3.a
print(link["href"])
print(link["title"])
print(card["data-id"])
print(card.find("p", class_="star-rating")["class"])
print(link.get("rel"))
print(link.attrs)
