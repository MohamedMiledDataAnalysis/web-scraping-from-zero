import requests

r = requests.get("http://localhost:8000/api/v1/stations",
                 headers={"X-API-Key": "pg-demo-2027"},
                 params={"country": "UK"}, timeout=10)
r.raise_for_status()
print([s["name"] for s in r.json()["stations"]])
