import csv

books = [
    {"title": "The Broken Forest", "author": "Nadia Kowal", "price": 26.93},
    {"title": "Salt Kingdom", "author": "Omar Hartley", "price": 19.2},
]

with open("output/books.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "author", "price"])
    writer.writeheader()
    writer.writerows(books)

print(open("output/books.csv", encoding="utf-8").read())
