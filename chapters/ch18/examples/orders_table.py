from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE = "http://localhost:8000"
session = requests.Session()
page = BeautifulSoup(
    session.get(f"{BASE}/account/login", timeout=10).text, "html.parser"
)
session.post(
    f"{BASE}/account/login",
    timeout=10,
    data={
        "csrf_token": page.select_one('input[name="csrf_token"]')[
            "value"
        ],
        "username": "reader",
        "password": "practice",
    },
)
html = session.get(f"{BASE}/account/", timeout=10).text
orders = pd.read_html(StringIO(html), attrs={"id": "orders"})[0]
print(orders.head(3).to_string(index=False))
print(orders["Status"].value_counts().to_string())
session.get(f"{BASE}/account/logout", timeout=10)
print("After logout:", session.get(f"{BASE}/account/", timeout=10).url)
