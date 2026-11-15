prices = ["£26.93", " £1,049.00", "£6.56 ", "£19.20"]
numbers = []
for p in prices:
    clean = p.strip().replace("£", "").replace(",", "")
    numbers.append(float(clean))
print(numbers)
print(max(numbers))
print(round(sum(numbers) / len(numbers), 2))
