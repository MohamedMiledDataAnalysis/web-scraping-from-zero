import json
import re

import requests

html = requests.get("http://localhost:8000/quotes/js/page/2/", timeout=10).text
match = re.search(r"var data = (\[.*?\]);", html, re.DOTALL)
quotes = json.loads(match.group(1))
print(len(quotes))
print(sorted({q["author"] for q in quotes}))
