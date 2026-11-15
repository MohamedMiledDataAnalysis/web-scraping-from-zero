import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/quotes/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")

first = soup.find("div", class_="quote")
print(first.find("span", class_="text").text)

quotes = soup.find_all("div", class_="quote")
print(len(quotes), "quotes")
for q in quotes[:3]:
    print("-", q.find("small", class_="author").text)
