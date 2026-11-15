def clean_price(text, symbol="£"):
    text = text.strip().replace(symbol, "").replace(",", "")
    return float(text)


print(clean_price("£19.20"))
print(clean_price("$45.00", symbol="$"))
