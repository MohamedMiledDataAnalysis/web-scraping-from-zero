availability = "In stock (19 available)"
print("stock" in availability)
parts = availability.split("(")
print(parts)
number = parts[1].replace(" available)", "")
print(int(number))
