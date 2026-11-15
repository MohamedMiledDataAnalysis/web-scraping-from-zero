import requests
from bs4 import BeautifulSoup

page = requests.get("http://localhost:8000/library/")  # 1. fetch
soup = BeautifulSoup(page.text, "html.parser")  # 2. parse
for card in soup.select("article.book-card"):  # 3. extract
    title = card.h3.a["title"]
    price = card.select_one(".price").text
    print(price, title)  # 4. save (here: print)
