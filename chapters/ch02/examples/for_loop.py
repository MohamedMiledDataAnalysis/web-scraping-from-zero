prices = ["£26.93", "£19.20", "£6.56"]
total = 0
for p in prices:
    value = float(p.replace("£", ""))
    total = total + value
    print(p, "->", value)
print("Total:", round(total, 2))
