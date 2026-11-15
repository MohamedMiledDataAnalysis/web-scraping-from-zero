from io import StringIO

import pandas as pd
import requests

html = requests.get("http://localhost:8000/tables/", timeout=10).text
league = pd.read_html(StringIO(html), attrs={"id": "league-table"})[0]
print(list(league.columns)[:3])

league.columns = [b if a == b else f"{a} {b}" for a, b in league.columns]
print(list(league.columns))
print(league[["Team", "Results Won", "Points"]].head(3).to_string())
