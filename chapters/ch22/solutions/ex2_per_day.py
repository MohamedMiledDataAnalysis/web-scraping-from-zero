import sqlite3

import pandas as pd

with sqlite3.connect("output/ch22/jobs.db") as db:
    print(pd.read_sql("SELECT day, COUNT(*) AS jobs FROM jobs GROUP BY day ORDER BY day",
                      db).to_string(index=False))
