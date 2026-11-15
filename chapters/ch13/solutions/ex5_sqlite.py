import sqlite3

import pandas as pd

books = pd.read_csv("output/ch13/books_p1_p2.csv")
words = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
books["rating"] = books["rating"].map(words)
with sqlite3.connect("output/ch13/books.db") as db:
    books.to_sql("books", db, if_exists="replace", index=False)
    query = """
        SELECT rating, COUNT(*) AS books, ROUND(AVG(price), 2) AS avg_price
        FROM books GROUP BY rating ORDER BY rating DESC
    """
    print(pd.read_sql(query, db).to_string(index=False))
