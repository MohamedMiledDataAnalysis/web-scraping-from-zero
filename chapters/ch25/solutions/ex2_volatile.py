import sqlite3

import pandas as pd

with sqlite3.connect("output/ch25/prices.db") as db:
    hist = pd.read_sql("SELECT name, price FROM prices", db)
spread = hist.groupby("name")["price"].agg(["min", "max"])
spread["gap_pct"] = ((spread["max"] / spread["min"] - 1) * 100).round(1)
print(spread.sort_values("gap_pct", ascending=False).head(1).to_string())
