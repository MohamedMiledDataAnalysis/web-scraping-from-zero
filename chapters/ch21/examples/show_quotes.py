import json

quotes = json.load(open("output/ch21/quotes.json", encoding="utf-8"))
print(len(quotes), "quotes")
print(quotes[0])
