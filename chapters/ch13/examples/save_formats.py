import sqlite3
from pathlib import Path

import pandas as pd

out = Path("output/ch13")
out.mkdir(parents=True, exist_ok=True)
books = pd.DataFrame(
    {
        "title": ["The Broken Forest", "Salt Kingdom"],
        "price": [26.93, 19.20],
        "tags": [["history", "forest"], ["music"]],
    }
)

books.drop(columns="tags").to_csv(out / "books.csv", index=False)
books.drop(columns="tags").to_excel(out / "books.xlsx", index=False)
books.to_json(
    out / "books.json", orient="records", indent=2, force_ascii=False
)

with sqlite3.connect(out / "books.db") as db:
    books.drop(columns="tags").to_sql(
        "books", db, if_exists="replace", index=False
    )
    print(
        pd.read_sql(
            "SELECT title, price FROM books WHERE price > 20", db
        ).to_string()
    )

print((out / "books.json").read_text(encoding="utf-8")[:80])
