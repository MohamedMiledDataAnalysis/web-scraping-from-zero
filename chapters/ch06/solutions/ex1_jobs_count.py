import requests
from bs4 import BeautifulSoup

for day in ["", "2027-03-15"]:
    url = "http://localhost:8000/jobs/"
    if day:
        url += "?day=" + day
    soup = BeautifulSoup(requests.get(url, timeout=10).text, "html.parser")
    print(day or "site date", "->", soup.select_one(".result-count").text)
