import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
print("Site date:", soup.find(id="site-date").text)

html = requests.get("http://localhost:8000/jobs/?day=2027-03-10", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
print(soup.select_one(".site-date").text.strip())
print(soup.select_one(".result-count").text)
