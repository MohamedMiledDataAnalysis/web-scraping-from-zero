from io import StringIO

import pandas as pd
import requests

html = requests.get("http://localhost:8000/tables/", timeout=10).text
league = pd.read_html(StringIO(html), attrs={"id": "league-table"})[0]
print(league.to_string())
