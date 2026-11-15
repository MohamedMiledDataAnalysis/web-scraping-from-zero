import requests

url = "http://localhost:8000/shop/api/products"
for params in [
    {"per_page": 50},
    {"per_page": 500},
    {"sort": "price", "per_page": 3},
    {"category": "Garden", "per_page": 1},
    {"page": 99},
]:
    data = requests.get(url, params=params, timeout=10).json()
    names = [p["name"] for p in data["products"]]
    print(params, "->", data["pages"], "pages,", len(names), names[:3])
