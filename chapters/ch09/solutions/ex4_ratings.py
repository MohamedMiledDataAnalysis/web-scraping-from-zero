import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/library/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
counts = {w: 0 for w in ["One", "Two", "Three", "Four", "Five"]}
for p in soup.find_all("p", class_="star-rating"):
    word = p["class"][1]
    counts[word] += 1
print(counts)
