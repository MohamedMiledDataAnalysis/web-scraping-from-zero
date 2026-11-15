import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/quotes/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")

rows = []
for q in soup.find_all("div", class_="quote"):
    rows.append({
        "text": q.find("span", class_="text").text,
        "author": q.find("small", class_="author").text,
        "tags": [a.text for a in q.find_all("a", class_="tag")],
    })
print(len(rows))
print(rows[0])
