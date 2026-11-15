import requests
from bs4 import BeautifulSoup

r = requests.post(
    "http://localhost:8000/account/login",
    data={"username": "reader", "password": "practice"},
    timeout=10,
)
print(r.status_code)
print(BeautifulSoup(r.text, "html.parser").select_one("p.error").text)
