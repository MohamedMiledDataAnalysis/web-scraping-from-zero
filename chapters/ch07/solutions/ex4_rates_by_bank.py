from io import StringIO

import pandas as pd
import requests

html = requests.get("http://localhost:8000/tables/", timeout=10).text
rates = pd.read_html(StringIO(html), match="Minimum deposit",
                     na_values=["n/a"])[0]
rates["Rate"] = rates["Rate"].str.rstrip("%").astype(float)
average = rates.groupby("Bank")["Rate"].mean().sort_values(ascending=False)
print(average.round(2))
