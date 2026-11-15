from urllib.parse import urljoin

import pandas as pd
import requests

BASE = "http://localhost:8000"
session = requests.Session()
session.headers["X-API-Key"] = "pg-demo-2027"

url = BASE + "/api/v1/observations"
params = {"station": "EDI", "start": "2027-01-01", "end": "2027-01-31"}
rows = []
while url:
    r = session.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    rows += data["results"]
    print(
        f"page {data['page']} of {data['pages']}: "
        f"{len(data['results'])} days"
    )
    url = urljoin(BASE, data["next"]) if data["next"] else None
    params = None  # the next address already contains them

weather = pd.DataFrame(rows)
print(len(weather), "days")
print(weather.head(3).to_string(index=False))
print("Rainy days:", (weather["rain_mm"] > 0).sum())
