import sqlite3

import pandas as pd

with sqlite3.connect("output/ch24/tracker.db") as db:
    print(pd.read_sql("SELECT city, COUNT(*) AS jobs FROM jobs GROUP BY city "
                      "ORDER BY jobs DESC, city", db).to_string(index=False))
