from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

url = "http://localhost:8000/quotes/"
soup = BeautifulSoup(requests.get(url, timeout=10).text, "html.parser")
for q in soup.find_all("div", class_="quote"):
    author = q.find("small", class_="author").text
    about = q.find("span", class_="by").find("a")["href"]
    print(author, urljoin(url, about))
