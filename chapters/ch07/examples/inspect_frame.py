from io import StringIO

import pandas as pd
import requests

html = requests.get("http://localhost:8000/tables/", timeout=10).text
planets = pd.read_html(StringIO(html), thousands=",")[0]
print(planets.shape)
print(list(planets.columns))
print(planets.dtypes)
print(planets.head(3).to_string())
print(planets["Diameter (km)"].max())
