import requests

data = requests.get("http://localhost:8000/shop/api/products",
                    params={"category": "Office", "sort": "rating", "per_page": 3},
                    timeout=10).json()
for p in data["products"]:
    print(p["rating"], p["name"])
