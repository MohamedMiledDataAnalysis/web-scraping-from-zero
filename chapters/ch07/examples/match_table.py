from io import StringIO

import pandas as pd
import requests

html = requests.get("http://localhost:8000/tables/", timeout=10).text
rates = pd.read_html(StringIO(html), match="Minimum deposit")
print(len(rates))
print(rates[0].to_string())
