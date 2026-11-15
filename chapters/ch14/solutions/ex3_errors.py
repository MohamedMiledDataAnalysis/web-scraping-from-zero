import requests

url = "http://localhost:8000/api/v1/observations"
headers = {"X-API-Key": "pg-demo-2027"}
for params in [{"station": "XYZ"},
               {"station": "LON", "start": "2027-03-01", "end": "2027-02-01"}]:
    r = requests.get(url, params=params, headers=headers, timeout=10)
    print(r.status_code, r.json()["error"])
