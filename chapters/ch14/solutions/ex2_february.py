from urllib.parse import urljoin

import pandas as pd
import requests

BASE = "http://localhost:8000"
session = requests.Session()
session.headers["X-API-Key"] = "pg-demo-2027"
url = BASE + "/api/v1/observations"
params = {"station": "LON", "start": "2027-02-01", "end": "2027-02-28"}
rows = []
while url:
    data = session.get(url, params=params, timeout=10).json()
    rows += data["results"]
    url = urljoin(BASE, data["next"]) if data["next"] else None
    params = None
df = pd.DataFrame(rows)
warmest = df.loc[df["temp_max_c"].idxmax()]
print(len(df), "days; warmest:", warmest["temp_max_c"], "on", warmest["date"])
