import requests
from bs4 import BeautifulSoup

url = "http://localhost:8000/library/book/salt-kingdom-2.html"
soup = BeautifulSoup(requests.get(url, timeout=10).text, "html.parser")

label = soup.find("th", string="Availability")
print(label.find_next_sibling("td").text)

info = {}
for row in soup.find("table", class_="info").find_all("tr"):
    info[row.th.text] = row.td.text
print(info)
