import sqlite3
import sys
from io import StringIO
from pathlib import Path

import pandas as pd

sys.path.insert(0, ".")
from toolkit.polite import PoliteClient  # noqa: E402

DB = "output/ch25/backfill.db"
Path(DB).unlink(missing_ok=True)
client = PoliteClient("PriceMonitor/1.0 (+mailto:reader@example.com)", delay=0.2)
watch = pd.read_csv("output/ch25/watchlist.csv")
frames = []
for w in watch.itertuples():
    html = client.get(f"http://localhost:8000/prices/item/{w.id}/?day=2027-03-01").text
    hist = pd.read_html(StringIO(html), attrs={"id": "history"})[0]
    hist["price"] = hist["Price"].str.lstrip("£").astype(float)
    frames.append(hist.rename(columns={"Date": "day"})[["day"]]
                  .assign(id=w.id, name=w.name, price=hist["price"]))
history = pd.concat(frames)
with sqlite3.connect(DB) as db:
    history.to_sql("prices", db, if_exists="replace", index=False)
print(len(history), "rows from", len(watch), "requests")
print(history.groupby("name")["price"].agg(["min", "max"]).round(2).to_string())
