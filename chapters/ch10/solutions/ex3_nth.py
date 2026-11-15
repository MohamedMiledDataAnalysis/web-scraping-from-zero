import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/tables/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
last = soup.select_one("#planets-table tbody tr:last-of-type")
print(
    [
        td.text
        for td in last.select("td:nth-of-type(1), td:nth-of-type(3)")
    ]
)
row = soup.select_one("#rates-table tr:nth-of-type(3)")
print(row.get_text(" | ", strip=True))
