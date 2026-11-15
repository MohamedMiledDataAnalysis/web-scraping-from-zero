import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/prices/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
for row in soup.select("#prices tbody tr")[:3]:
    print(row["data-id"], row.td.a.text, row.select_one("td.price").text)
