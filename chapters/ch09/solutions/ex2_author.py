import requests
from bs4 import BeautifulSoup

url = "http://localhost:8000/quotes/author/tomas-reyna/"
soup = BeautifulSoup(requests.get(url, timeout=10).text, "html.parser")
name = soup.find("h1", class_="author-title").text
born = soup.find("span", class_="author-born-date").text
place = soup.find("span", class_="author-born-location").text
print(f"{name}, born {born} in {place}")
