import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/library/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
for a in soup.select("article.book-card:has(.star-rating.Five) h3 a"):
    print(a["title"])
