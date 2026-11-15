import pandas as pd
import requests

data = requests.get("http://localhost:8000/shop/api/products",
                    params={"per_page": 5}, timeout=10).json()
products = pd.json_normalize(data["products"])
print(list(products.columns))
print(products.loc[products["in_stock"], "name"].tolist())
