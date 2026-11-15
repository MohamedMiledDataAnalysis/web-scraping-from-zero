import time

import pandas as pd
import requests

session = requests.Session()
url = "http://localhost:8000/shop/api/products"
products, page, pages = [], 1, 1
while page <= pages:
    data = session.get(url, params={"page": page}, timeout=10).json()
    products += data["products"]
    pages = data["pages"]
    page += 1
    time.sleep(0.2)

df = pd.DataFrame(products)
print(len(df), "products in", pages, "requests")
print(df.groupby("category")["price"].agg(["count", "mean", "max"]).round(2).to_string())
