import sqlite3

import pandas as pd

query = """
    SELECT title, city, first_seen, last_seen,
           julianday(last_seen) - julianday(first_seen) + 1 AS days
    FROM jobs WHERE last_seen < '2027-03-07' AND days <= 2 ORDER BY first_seen, title
"""
with sqlite3.connect("output/ch24/tracker.db") as db:
    print(pd.read_sql(query, db).to_string(index=False))
