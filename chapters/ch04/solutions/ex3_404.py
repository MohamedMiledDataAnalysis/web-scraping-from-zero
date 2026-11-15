import requests
from bs4 import BeautifulSoup

r = requests.get("http://localhost:8000/library/page-51.html")
print(r.status_code, r.ok)
soup = BeautifulSoup(r.text, "html.parser")
print(soup.h1.text)
