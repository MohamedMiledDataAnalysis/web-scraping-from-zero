import os

import requests

key = os.environ.get("PG_API_KEY", "pg-demo-2027")
r = requests.get("http://localhost:8000/api/v1/stations",
                 headers={"X-API-Key": key}, params={"country": "FR"}, timeout=10)
print([s["name"] for s in r.json()["stations"]])
