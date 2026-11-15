def safe_price(text):
    """Return the price as a number, or None if the text is not a price."""
    clean = text.replace("£", "").replace(",", "").replace(" ", "")
    try:
        return float(clean)
    except ValueError:
        return None


raw = ["£24.99", "", "£ 18.50", "N/A", "£1,049.00"]
prices = [safe_price(t) for t in raw]
print(prices)
print(prices.count(None), "prices could not be read")
