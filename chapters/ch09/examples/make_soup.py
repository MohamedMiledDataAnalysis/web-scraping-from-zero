import requests
from bs4 import BeautifulSoup

session = requests.Session()
html = session.get("http://localhost:8000/quotes/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
print(soup.title)
print(soup.title.text)
print(soup.h1.text)
