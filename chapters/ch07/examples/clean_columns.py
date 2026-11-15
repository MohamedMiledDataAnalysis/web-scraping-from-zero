from io import StringIO

import pandas as pd
import requests

html = requests.get("http://localhost:8000/tables/", timeout=10).text
tables = pd.read_html(StringIO(html), na_values=["n/a"])
league, rates = tables[1], tables[2]

league.columns = [b if a == b else f"{a} {b}" for a, b in league.columns]
league["Team"] = league["Team"].str.replace(r"\[.*\]", "", regex=True)
print(league["Team"].tolist())

rates["Rate"] = rates["Rate"].str.rstrip("%").astype(float)
rates["Minimum deposit"] = (rates["Minimum deposit"]
                            .str.replace("£", "").str.replace(",", "")
                            .astype(int))
print(rates.dtypes)
print(rates.sort_values("Rate", ascending=False).head(2).to_string())
