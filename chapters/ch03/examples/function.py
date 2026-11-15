def clean_price(text):
    """Turn a price such as ' £1,049.00 ' into the number 1049.0."""
    text = text.strip().replace("£", "").replace(",", "")
    return float(text)


print(clean_price("£26.93"))
print(clean_price(" £1,049.00 "))
prices = [clean_price(p) for p in ["£5.00", "£12.50"]]
print(prices)
