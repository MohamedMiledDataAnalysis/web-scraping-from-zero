import requests
from bs4 import BeautifulSoup

r = requests.get(
    "http://localhost:8000/jobs/",
    params={"q": "python", "city": "London"},
    timeout=10,
)
print(r.url)
print(
    BeautifulSoup(r.text, "html.parser")
    .select_one(".result-count")
    .text
)
