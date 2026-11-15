from pathlib import Path

import pandas as pd
import requests

out = Path("output/ch08")
out.mkdir(parents=True, exist_ok=True)
url = "http://localhost:8000/files/monthly_sales.csv"
r = requests.get(url, timeout=30)
r.raise_for_status()
path = out / "monthly_sales.csv"
path.write_bytes(r.content)
print(path, path.stat().st_size, "bytes")
sales = pd.read_csv(path)
print(sales.groupby("region")["revenue_gbp"].sum().round(2).to_string())
