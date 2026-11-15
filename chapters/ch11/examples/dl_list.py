import requests
from bs4 import BeautifulSoup

url = "http://localhost:8000/jobs/1252/"
soup = BeautifulSoup(requests.get(url, timeout=10).text, "html.parser")
labels = [dt.text for dt in soup.select("dl dt")]
values = [dd.get_text(" ", strip=True) for dd in soup.select("dl dd")]
job = dict(zip(labels, values))
job["title"] = soup.h1.text
print(job)
