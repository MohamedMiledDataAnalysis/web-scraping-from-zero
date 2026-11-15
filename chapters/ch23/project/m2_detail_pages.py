"""Method 2: requests + JSON-LD on the 1,000 detail pages."""

import csv
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, ".")
sys.path.insert(0, "chapters/ch12/examples")
from book_parser import parse_book_page  # noqa: E402
from toolkit.polite import PoliteClient  # noqa: E402

OUT = Path("output/ch23")
progress = OUT / "m2_progress.csv"
client = PoliteClient(
    "LearningScraper/1.0 (+mailto:reader@example.com)", delay=0.2
)

urls = pd.read_csv(OUT / "m1_list_pages.csv")[
    "url"
].tolist()  # from method 1
done = set(pd.read_csv(progress)["url"]) if progress.exists() else set()
fields = [
    "url",
    "title",
    "author",
    "category",
    "price",
    "rating",
    "stock",
    "pages",
    "year",
]
sent = 0
with open(progress, "a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    if not done:
        writer.writeheader()
    for url in urls:
        if url in done:
            continue
        writer.writerow(parse_book_page(url, client.get(url).text))
        sent += 1
        f.flush()

books = pd.read_csv(progress)
books.to_csv(OUT / "m2_detail_pages.csv", index=False)
(OUT / "m2_meta.json").write_text(
    json.dumps({"requests": len(books) + 1})
)
print(
    len(books),
    "books,",
    len(books.columns),
    "columns; sent this run:",
    sent,
)
