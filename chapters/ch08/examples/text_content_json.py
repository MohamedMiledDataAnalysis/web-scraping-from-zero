import requests

page = requests.get("http://localhost:8000/library/", timeout=10)
print(type(page.text), page.text[:15])
print(type(page.content), page.content[:15])

api = requests.get("http://localhost:8000/shop/api/products?per_page=2", timeout=10)
data = api.json()
print(type(data), data["total"], data["products"][0]["name"])
