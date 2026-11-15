import json

quote = {"author": "Rashid Noor",
         "text": "The wrong answer shows you where to look.",
         "tags": ["failure", "questions"]}

with open("output/quote.json", "w", encoding="utf-8") as f:
    json.dump(quote, f, indent=2, ensure_ascii=False)

with open("output/quote.json", encoding="utf-8") as f:
    back = json.load(f)
print(back["tags"][1])
print(json.dumps(back, ensure_ascii=False))
