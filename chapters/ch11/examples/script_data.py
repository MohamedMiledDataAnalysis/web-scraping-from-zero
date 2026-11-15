import json
import re

import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/quotes/js/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
script = soup.find("script", string=re.compile(r"var data ="))
match = re.search(r"var data = (\[.*?\]);", script.string, re.DOTALL)
quotes = json.loads(match.group(1))
print(len(quotes), "quotes")
print(quotes[0]["author"], "-", quotes[0]["text"])
