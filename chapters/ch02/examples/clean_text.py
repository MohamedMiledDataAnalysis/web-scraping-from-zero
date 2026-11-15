raw = "   £1,049.00\n "
print(repr(raw))
print(repr(raw.strip()))
print(raw.strip().replace("£", "").replace(",", ""))
print(float(raw.strip().replace("£", "").replace(",", "")))
