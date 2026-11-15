from pathlib import Path

import pandas as pd

source = Path("output/ch23/m2_detail_pages.csv")
if not source.exists():
    raise SystemExit(
        "Run m1_list_pages.py and m2_detail_pages.py (Chapter 23) first."
    )
books = pd.read_csv(source)

problems = []
if len(books) != 1000:
    problems.append(f"{len(books)} books")
if books[["price", "pages"]].isna().any().any():
    problems.append("missing price or pages")
if (books["price"] <= 0).any():
    problems.append("price <= 0")
if books["url"].duplicated().any():
    problems.append("duplicate urls")
if problems:
    raise SystemExit("Checks failed: " + "; ".join(problems))

data = books[books["stock"] > 0].copy()
data["pages_per_pound"] = (data["pages"] / data["price"]).round(2)
out = Path("output/ch26/dataset")
out.mkdir(parents=True, exist_ok=True)
columns = [
    "title",
    "author",
    "category",
    "price",
    "pages",
    "stock",
    "year",
    "pages_per_pound",
    "url",
]
data[columns].sort_values(["category", "title"]).to_csv(
    out / "library_value.csv", index=False
)
print(
    "Checks passed;",
    len(data),
    "books in stock kept out of",
    len(books),
)
