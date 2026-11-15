book = {
    "title": "The Broken Forest",
    "author": "Nadia Kowal",
    "price": 26.93,
    "rating": 3,
}
print(book["title"])
print(book["price"] * 2)
book["in_stock"] = True          # add a new key
book["price"] = 24.99            # change a value
print(book)
print(list(book.keys()))
