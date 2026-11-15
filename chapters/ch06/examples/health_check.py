import requests
from bs4 import BeautifulSoup

BASE = "http://localhost:8000"
sections = ["/", "/library/", "/quotes/", "/tables/", "/api/", "/shop/",
            "/account/login", "/files/", "/jobs/", "/prices/", "/trouble/"]

for path in sections:
    r = requests.get(BASE + path, timeout=10)
    title = BeautifulSoup(r.text, "html.parser").title.text
    print(f"{r.status_code}  {path:<15} {title}")
