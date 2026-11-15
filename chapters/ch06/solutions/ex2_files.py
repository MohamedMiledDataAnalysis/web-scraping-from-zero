import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/files/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
for row in soup.select("#file-list tbody tr"):
    name, size = [td.text for td in row.find_all("td")]
    print(f"{name:<30} {int(size):>7,} bytes")
