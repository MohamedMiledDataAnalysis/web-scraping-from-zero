import re

text = "In stock (19 available) - shipped in 2 days"
print(re.search(r"\((\d+) available\)", text).group(1))
print(re.findall(r"\d+", text))
print(re.sub(r"\s+", " ", "  too   many \n spaces ").strip())
print(bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", "2027-03-01")))
