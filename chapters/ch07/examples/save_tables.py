from io import StringIO
from pathlib import Path

import pandas as pd
import requests

out = Path("output/ch07")
out.mkdir(parents=True, exist_ok=True)

html = requests.get("http://localhost:8000/tables/", timeout=10).text
planets = pd.read_html(StringIO(html), thousands=",")[0]
planets.to_csv(out / "planets.csv", index=False)
planets.to_excel(out / "planets.xlsx", index=False, sheet_name="Planets")
print(pd.read_csv(out / "planets.csv").tail(2).to_string())
