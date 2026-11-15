import requests
from bs4 import BeautifulSoup

url = "http://localhost:8000/library/page-2.html"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")
for card in soup.select("article.book-card"):
    title = card.h3.a["title"]
    price = card.select_one(".price").text
    print(price, title)
