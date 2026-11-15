import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/library/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
prices = soup.select("article.book-card p.price")
print(len(prices), prices[0].text)
print(soup.select_one("#site-date"))
print(soup.select_one("p.result-count").text)
