from io import StringIO

import pandas as pd
import requests

html = requests.get("http://localhost:8000/tables/", timeout=10).text
tables = pd.read_html(StringIO(html))
print(len(tables), "tables found")
planets = tables[0]
print(planets.to_string())
