from pathlib import Path

import pandas as pd

folder = Path("output/ch26/dataset")
data = pd.read_csv(folder / "library_value.csv")
meaning = {
    "title": ("text", "", "book title, from JSON-LD `name`"),
    "author": ("text", "", "author, from JSON-LD `author.name`"),
    "category": ("text", "", "library category, from JSON-LD `genre`"),
    "price": ("number", "GBP", "price, from JSON-LD `offers.price`"),
    "pages": ("integer", "pages", "from JSON-LD `numberOfPages`"),
    "stock": ("integer", "copies", "from the information table, *Availability*"),
    "year": ("integer", "year", "from JSON-LD `datePublished`"),
    "pages_per_pound": ("number", "pages/GBP", "pages divided by price, 2 decimals"),
    "url": ("text", "", "address of the book's page"),
}
lines = ["| Column | Type | Unit | Meaning and source | Example |", "|---|---|---|---|---|"]
for col in data.columns:
    kind, unit, text = meaning[col]
    lines.append(f"| {col} | {kind} | {unit} | {text} | {data[col].iloc[0]} |")
(folder / "DATA_DICTIONARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

readme = f"""# Library value dataset

{len(data)} books in stock from the Practice Ground library, with pages per pound.

- Collected: 2027-03-01 (site date), by `chapters/ch23/project/m2_detail_pages.py`
- Source and terms: Practice Ground, learning use; all data is invented
- Checks: 1000 books collected, no missing price or pages, prices above 0, unique urls
- Update: rerun the Chapter 23 scrapers, then `build_dataset.py` and `document.py`
- Limits: books out of stock are excluded; prices are those of the collection day
- Licence: MIT for the code; the data is invented and free to reuse with credit
"""
(folder / "README.md").write_text(readme, encoding="utf-8")
print((folder / "DATA_DICTIONARY.md").read_text(encoding="utf-8").splitlines()[2])
print(sorted(p.name for p in folder.iterdir()))
