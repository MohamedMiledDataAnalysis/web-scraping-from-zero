import requests
from bs4 import BeautifulSoup

url = "http://localhost:8000/library/book/salt-kingdom-2.html"
soup = BeautifulSoup(requests.get(url).text, "html.parser")
for script in soup.find_all("script"):
    print(script.get("type"))
