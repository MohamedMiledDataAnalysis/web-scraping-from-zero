import requests

session = requests.Session()
for pid in [7, 8, 9]:
    p = session.get(f"http://localhost:8000/shop/api/product/{pid}", timeout=10).json()
    print(pid, p["name"], p["price"], p["reviews"])
