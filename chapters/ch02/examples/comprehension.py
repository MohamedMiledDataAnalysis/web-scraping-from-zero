prices = ["£26.93", "£19.20", "£6.56", "£59.27"]
numbers = [float(p.replace("£", "")) for p in prices]
print(numbers)
cheap = [n for n in numbers if n < 20]
print(cheap)
