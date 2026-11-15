import requests

url = "http://localhost:8000/shop/api/products"
r = requests.get(
    url, params={"page": 1, "category": "", "sort": "id"}, timeout=10
)
r.raise_for_status()
data = r.json()
print(data["page"], data["pages"], data["total"])
for p in data["products"][:3]:
    print(p["sku"], p["name"], p["price"], p["in_stock"])
