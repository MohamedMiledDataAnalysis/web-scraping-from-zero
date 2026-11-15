import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/trouble/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
for item in soup.select("ul.trouble-list li")[:3]:
    link = item.a["href"]
    explanation = item.get_text().split(":", 1)[1].strip()
    print(link, "", explanation)
