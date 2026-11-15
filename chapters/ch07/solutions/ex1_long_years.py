from io import StringIO

import pandas as pd
import requests

html = requests.get("http://localhost:8000/tables/", timeout=10).text
planets = pd.read_html(StringIO(html), thousands=",")[0]
long_years = planets[planets["Orbital period (days)"] > 1000]
print(long_years["Planet"].tolist())
