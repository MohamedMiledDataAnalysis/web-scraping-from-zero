import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/trouble/messy-cards", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
for card in soup.find_all("div", class_="card"):
    name = card.find("h3", class_="name").text
    price = card.find("span", class_="price").text
    print(name, price)
