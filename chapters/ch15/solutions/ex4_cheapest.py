import time

import pandas as pd
import requests

session = requests.Session()
URL = "http://localhost:8000/shop/api/products"


def all_pages(url, params):
    items, page, pages = [], 1, 1
    while page <= pages:
        data = session.get(
            url,
            params={**params, "page": page, "per_page": 50},
            timeout=10,
        ).json()
        items += data["products"]
        pages = data["pages"]
        page += 1
        time.sleep(0.2)
    return items


for category in ["Audio", "Garden", "Kitchen", "Office"]:
    df = pd.DataFrame(
        all_pages(URL, {"category": category, "sort": "price"})
    )
    cheapest = df[df["in_stock"]].iloc[0]
    print(
        f"{category:<8} {cheapest['name']:<20} £{cheapest['price']:.2f}"
    )
