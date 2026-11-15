import requests
from bs4 import BeautifulSoup

BASE = "http://localhost:8000"
session = requests.Session()
page = BeautifulSoup(
    session.get(f"{BASE}/account/login", timeout=10).text, "html.parser"
)
print("Cookies after the login page:", list(session.cookies.keys()))
token = page.select_one('input[name="csrf_token"]')["value"]
session.post(
    f"{BASE}/account/login",
    timeout=10,
    data={
        "csrf_token": token,
        "username": "reader",
        "password": "practice",
    },
)

orders = session.get(f"{BASE}/account/", timeout=10)
print("With the session:", orders.url)
plain = requests.get(f"{BASE}/account/", timeout=10)
print("Without it:", plain.url)

csv_text = session.get(f"{BASE}/account/orders.csv", timeout=10).text
print(csv_text.splitlines()[0])
print(len(csv_text.splitlines()) - 1, "orders")
