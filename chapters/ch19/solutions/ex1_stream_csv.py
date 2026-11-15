from pathlib import Path

import pandas as pd
import requests

path = Path("output/ch19/monthly_sales.csv")
path.parent.mkdir(parents=True, exist_ok=True)
with requests.get("http://localhost:8000/files/monthly_sales.csv",
                  stream=True, timeout=60) as r:
    r.raise_for_status()
    assert r.headers["Content-Type"].startswith("text/csv"), r.headers["Content-Type"]
    with open(path, "wb") as f:
        for chunk in r.iter_content(65536):
            f.write(chunk)
sales = pd.read_csv(path)
north = sales[sales["region"] == "North"]
best = north.loc[north["revenue_gbp"].idxmax()]
print(best["month"], best["revenue_gbp"])
