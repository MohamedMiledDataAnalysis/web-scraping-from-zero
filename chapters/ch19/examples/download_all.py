from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

out = Path("output/ch19/files")
out.mkdir(parents=True, exist_ok=True)
session = requests.Session()
page = "http://localhost:8000/files/"
soup = BeautifulSoup(session.get(page, timeout=10).text, "html.parser")

for a in soup.select("#file-list a"):
    url = urljoin(page, a["href"])
    with session.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        kind = r.headers.get("Content-Type", "").split(";")[0]
        path = out / Path(url).name
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=64 * 1024):
                f.write(chunk)
    print(f"{path.name:<30} {kind:<70} {path.stat().st_size:>6} bytes")
