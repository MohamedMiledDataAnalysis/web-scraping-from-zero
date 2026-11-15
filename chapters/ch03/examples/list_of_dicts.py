books = []
books.append({"title": "The Broken Forest", "price": 26.93})
books.append({"title": "Salt Kingdom", "price": 19.20})
books.append({"title": "A River of Maps", "price": 6.56})

print(len(books), "books")
for b in books:
    print(f'{b["title"]:<20} £{b["price"]:.2f}')
cheapest = min(books, key=lambda b: b["price"])
print("Cheapest:", cheapest["title"])
