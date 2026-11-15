"""The final catalogue: data and summary sheets in one Excel file."""

from pathlib import Path

import pandas as pd

OUT = Path("output/ch23")
books = pd.read_csv(OUT / "m2_detail_pages.csv")
books = books.sort_values(["category", "title"]).reset_index(drop=True)

problems = []
if len(books) != 1000:
    problems.append(f"{len(books)} books instead of 1000")
if books["url"].duplicated().any():
    problems.append("duplicate books")
if books[["price", "rating", "stock"]].isna().any().any():
    problems.append("missing values")
print("Checks:", problems or "all passed")

summary = (
    books.groupby("category")
    .agg(
        books=("title", "count"),
        avg_price=("price", "mean"),
        avg_rating=("rating", "mean"),
        stock=("stock", "sum"),
        out_of_stock=("stock", lambda s: (s == 0).sum()),
    )
    .round(2)
    .sort_values("books", ascending=False)
)

with pd.ExcelWriter(OUT / "catalogue.xlsx") as xl:
    books.to_excel(xl, sheet_name="Catalogue", index=False)
    summary.to_excel(xl, sheet_name="Summary")
print(summary.head(5).to_string())
print(
    "Cheapest five-star book:",
    books[books["rating"] == 5]
    .nsmallest(1, "price")[["title", "price"]]
    .values[0],
)
