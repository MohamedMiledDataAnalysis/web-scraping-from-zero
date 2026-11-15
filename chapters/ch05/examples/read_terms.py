import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/terms/").text
soup = BeautifulSoup(html, "html.parser")
words = ["robot", "scrap", "second", "commercial", "invented"]
for item in soup.select("ol.terms li"):
    text = item.get_text(" ", strip=True)
    found = [w for w in words if w in text.lower()]
    if found:
        print(found, "->", text)
