import requests
from bs4 import BeautifulSoup

BASE = "http://localhost:8000"
session = requests.Session()
session.headers["User-Agent"] = (
    "LearningScraper/1.0 (+mailto:reader@example.com)"
)

# 1. Load the login page and read the hidden token
page = BeautifulSoup(
    session.get(f"{BASE}/account/login", timeout=10).text, "html.parser"
)
token = page.select_one('input[name="csrf_token"]')["value"]

# 2. Send the form with the token
r = session.post(
    f"{BASE}/account/login",
    timeout=10,
    data={
        "csrf_token": token,
        "username": "reader",
        "password": "practice",
    },
)

# 3. Check that it worked
print(r.status_code, r.url)
print([h.status_code for h in r.history])
soup = BeautifulSoup(r.text, "html.parser")
print(soup.h1.get_text(" ", strip=True))
