import sqlite3

import pandas as pd

with sqlite3.connect("output/ch25/prices.db") as db:
    hist = pd.read_sql(
        "SELECT * FROM prices WHERE id IN (3, 7, 9, 14, 19) ORDER BY day",
        db,
    )
lowest = hist.loc[
    hist.groupby("name")["price"].idxmin(), ["name", "price", "day"]
]
print(lowest.sort_values("name").to_string(index=False))
