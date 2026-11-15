import requests
from bs4 import BeautifulSoup

BASE = "http://localhost:8000"


def login(session, username, password):
    page = BeautifulSoup(
        session.get(f"{BASE}/account/login", timeout=10).text,
        "html.parser",
    )
    token = page.select_one('input[name="csrf_token"]')["value"]
    r = session.post(
        f"{BASE}/account/login",
        timeout=10,
        data={
            "csrf_token": token,
            "username": username,
            "password": password,
        },
    )
    name = BeautifulSoup(r.text, "html.parser").select_one("#user-name")
    return name is not None and name.text == username


print(login(requests.Session(), "reader", "practice"))
print(login(requests.Session(), "reader", "wrong"))
