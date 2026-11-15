def clean_price(text):
    return float(text.strip().replace("£", "").replace(",", ""))


raw_prices = ["£24.99", "Price on request", "£18.50", ""]
for raw in raw_prices:
    try:
        price = clean_price(raw)
    except ValueError:
        price = None
        print(f"Could not read the price {raw!r}")
    print(price)
