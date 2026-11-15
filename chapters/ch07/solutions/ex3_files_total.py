from io import StringIO

import pandas as pd
import requests

html = requests.get("http://localhost:8000/files/", timeout=10).text
files = pd.read_html(StringIO(html), attrs={"id": "file-list"})[0]
print(files["Size (bytes)"].sum(), "bytes")
