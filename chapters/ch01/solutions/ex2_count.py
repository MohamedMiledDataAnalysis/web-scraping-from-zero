import requests
from bs4 import BeautifulSoup

page = requests.get("http://localhost:8000/library/")
soup = BeautifulSoup(page.text, "html.parser")
cards = soup.select("article.book-card")
print(len(cards), "books on page 1")
