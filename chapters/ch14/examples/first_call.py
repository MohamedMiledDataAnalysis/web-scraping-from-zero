import requests

API = "http://localhost:8000/api/v1"
headers = {"X-API-Key": "pg-demo-2027"}

r = requests.get(f"{API}/stations", headers=headers, timeout=10)
r.raise_for_status()
data = r.json()
print(data["count"], "stations")
for s in data["stations"]:
    print(s["id"], s["name"], s["country"])
print("Requests left:", r.headers["X-RateLimit-Remaining"])
