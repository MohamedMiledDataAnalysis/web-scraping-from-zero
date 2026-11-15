import sqlite3

import pandas as pd

query = """
    SELECT title, city, posted, last_seen,
           CAST(julianday(last_seen) - julianday(posted) + 1
                AS INTEGER) AS days
    FROM jobs WHERE last_seen < '2027-03-07' ORDER BY days, title
"""
with sqlite3.connect("output/ch24/tracker.db") as db:
    print(pd.read_sql(query, db).to_string(index=False))
