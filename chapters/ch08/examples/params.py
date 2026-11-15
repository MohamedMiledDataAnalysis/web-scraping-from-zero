import requests
from bs4 import BeautifulSoup

params = {"q": "data analyst", "city": "Leeds"}
response = requests.get(
    "http://localhost:8000/jobs/", params=params, timeout=10
)
print(response.url)
soup = BeautifulSoup(response.text, "html.parser")
print(soup.select_one(".result-count").text)
for job in soup.select("li.job h2 a")[:3]:
    print("-", job.text)
