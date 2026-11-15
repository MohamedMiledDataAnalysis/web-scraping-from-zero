import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/shop/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
print(len(soup.select("div.product")), "products found")
print(soup.select_one("#status").text)
print(soup.select_one("#products"))
print([s.get("src") for s in soup.find_all("script") if s.get("src")])
