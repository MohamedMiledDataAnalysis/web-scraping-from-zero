import csv
from pathlib import Path

quotes = [
    {"author": "Ada Fernhill", "text": "Small daily efforts build tall houses."},
    {"author": "Walter Pike", "text": "Measure the wood, not your worries."},
    {"author": "June Albright", "text": "Start the day with one good sentence."},
]

folder = Path("output/ch03")
folder.mkdir(parents=True, exist_ok=True)
path = folder / "quotes.csv"
with open(path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["author", "text"])
    writer.writeheader()
    writer.writerows(quotes)

with open(path, encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
print(len(rows), "rows")
print(rows[-1]["author"])
