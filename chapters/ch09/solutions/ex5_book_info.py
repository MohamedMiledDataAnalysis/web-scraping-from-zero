import requests
from bs4 import BeautifulSoup

url = "http://localhost:8000/library/book/the-broken-forest-1.html"
soup = BeautifulSoup(requests.get(url, timeout=10).text, "html.parser")
info = {row.th.text: row.td.text
        for row in soup.find("table", class_="info").find_all("tr")}
stock = int(info["Availability"].split("(")[1].split()[0])
pages = int(info["Pages"])
print(stock, pages)
