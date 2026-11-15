import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

session = requests.Session()
base = "http://localhost:8000/library/"
home = BeautifulSoup(session.get(base, timeout=10).text, "html.parser")
categories = {a.text: urljoin(base, a["href"])
              for a in home.select("aside.categories a")}
print(len(categories), "categories")

counts = {}
for name, url in categories.items():
    time.sleep(0.2)
    soup = BeautifulSoup(session.get(url, timeout=10).text, "html.parser")
    text = soup.select_one("p.result-count").text
    counts[name] = int(re.match(r"(\d+)", text).group(1))

for name, n in sorted(counts.items(), key=lambda kv: -kv[1])[:5]:
    print(f"{name:<16} {n}")
print("Total:", sum(counts.values()))
