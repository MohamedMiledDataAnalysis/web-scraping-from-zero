import time
from urllib.parse import urljoin

import pandas as pd
import requests

BASE = "http://localhost:8000"
session = requests.Session()
session.headers["X-API-Key"] = "pg-demo-2027"
limited = 0


def api_get(url, params=None):
    global limited
    while True:
        r = session.get(url, params=params, timeout=10)
        if r.status_code != 429:
            r.raise_for_status()
            return r.json()
        limited += 1
        time.sleep(int(r.headers.get("Retry-After", 5)))


rows = []
for station in ["LON", "MAN", "EDI", "PAR", "LYO"]:
    url = BASE + "/api/v1/observations"
    params = {"station": station, "start": "2027-01-01", "end": "2027-03-31"}
    while url:
        data = api_get(url, params)
        rows += data["results"]
        url = urljoin(BASE, data["next"]) if data["next"] else None
        params = None
        time.sleep(1.1)

df = pd.DataFrame(rows)
print(len(df), "observations")
print(df.groupby("station")["rain_mm"].sum().round(1).sort_values(ascending=False).to_string())
print("429 answers:", limited)
