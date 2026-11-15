import re

text = "Rooms: 3, floor 12, built 1998, price £245,000"
print(re.findall(r"\d+", text))
price = re.search(r"£([\d,]+)", text).group(1)
print(int(price.replace(",", "")))
