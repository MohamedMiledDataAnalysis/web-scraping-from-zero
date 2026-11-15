import time

import pandas as pd
import requests

session = requests.Session()
url = "http://localhost:8000/shop/api/products"
products, page, pages, calls = [], 1, 1, 0
while page <= pages:
    data = session.get(url, params={"page": page, "per_page": 50}, timeout=10).json()
    calls += 1
    products += data["products"]
    pages = data["pages"]
    page += 1
    time.sleep(0.2)
df = pd.DataFrame(products)
print(calls, "requests,", len(df), "products")
print((~df["in_stock"]).sum(), "out of stock")
top = df.loc[df["reviews"].idxmax()]
print("Most reviewed:", top["name"], top["reviews"])
