import requests
from bs4 import BeautifulSoup

page = requests.get("http://localhost:8000/library/")
soup = BeautifulSoup(page.text, "html.parser")
for card in soup.select("article.book-card"):
    title = card.h3.a["title"]
    price_text = card.select_one(".price").text
    price = float(price_text.replace("£", ""))
    if price < 15:
        print(price, title)
