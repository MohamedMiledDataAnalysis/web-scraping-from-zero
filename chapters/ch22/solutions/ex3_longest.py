import sqlite3

import pandas as pd

query = """
    SELECT id, title, company, COUNT(*) AS days, MIN(day) AS first_seen
    FROM jobs GROUP BY id ORDER BY days DESC, first_seen, id LIMIT 1
"""
with sqlite3.connect("output/ch22/jobs.db") as db:
    print(pd.read_sql(query, db).to_string(index=False))
