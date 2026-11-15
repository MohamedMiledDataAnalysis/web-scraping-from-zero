import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/quotes/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
box = soup.find("aside", class_="tag-box")
print(", ".join(a.text for a in box.find_all("a", class_="tag")))
