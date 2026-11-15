import csv

with open("output/books.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
print(rows[0])
print(type(rows[0]["price"]))
