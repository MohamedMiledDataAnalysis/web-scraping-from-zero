import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/library/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
copied = "body > main > div > section > div > article:nth-child(1) > p.price"
short = "article.book-card p.price"
print(soup.select_one(copied).text, len(soup.select(short)))

# The site adds a banner at the top of the grid: the copied one breaks.
banner = soup.new_tag("div", attrs={"class": "banner"})
soup.select_one("div.book-grid").insert(0, banner)
print(soup.select_one(copied), len(soup.select(short)))
