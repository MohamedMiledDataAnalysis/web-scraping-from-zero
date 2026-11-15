from io import StringIO

import pandas as pd
import requests

html = requests.get("http://localhost:8000/tables/", timeout=10).text
league = pd.read_html(StringIO(html), match="Points")[0]
league.columns = [
    b if a == b else f"{a} {b}" for a, b in league.columns
]
league["Team"] = league["Team"].str.replace(
    r"\s*\[[^\]]*\]", "", regex=True
)
print(league.loc[league["Points"] > 30, ["Team", "Points"]].to_string())
