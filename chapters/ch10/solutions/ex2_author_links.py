import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/quotes/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
links = soup.select('a[href*="/author/"]')
print(len(links), links[0]["href"])
