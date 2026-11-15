import requests
from bs4 import BeautifulSoup

page = requests.get("http://localhost:8000/library/")
soup = BeautifulSoup(page.text, "html.parser")
cards = soup.select("article.book-card")
for card in cards[:5]:
    title = card.h3.a["title"]
    author = card.select_one(".author").text
    print(title, "|", author)
