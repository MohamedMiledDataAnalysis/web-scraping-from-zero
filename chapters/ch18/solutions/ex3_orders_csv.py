from pathlib import Path

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
r = session.get(f"{BASE}/account/orders.csv", timeout=10)
r.raise_for_status()
path = Path("output/ch18/orders.csv")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_bytes(r.content)
orders = pd.read_csv(path)
print(f"Total: £{orders['total'].sum():.2f}")
print(
    orders.loc[
        orders["status"] == "On its way", ["number", "item"]
    ].to_string(index=False)
)
