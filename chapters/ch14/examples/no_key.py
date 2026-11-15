import requests

API = "http://localhost:8000/api/v1"
for headers in [{}, {"X-API-Key": "wrong"}]:
    r = requests.get(f"{API}/stations", headers=headers, timeout=10)
    print(r.status_code, r.json())
