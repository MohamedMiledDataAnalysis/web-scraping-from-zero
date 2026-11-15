import requests
from bs4 import BeautifulSoup

BASE = "http://localhost:8000"
session = requests.Session()
page = BeautifulSoup(session.get(f"{BASE}/account/login", timeout=10).text, "html.parser")
token = page.select_one('input[name="csrf_token"]')["value"]
r = session.post(f"{BASE}/account/login", timeout=10,
                 data={"csrf_token": token, "username": "reader", "password": "wrong"})
print(r.status_code, BeautifulSoup(r.text, "html.parser").select_one("p.error").text)
