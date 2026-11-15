import re

import pandas as pd

raw = ["£24.99", "  £ 18.50 ", None, "Price on request", "£1,049.00", "£7"]


def to_price(text):
    """'£1,049.00' -> 1049.0; anything that is not a price -> None."""
    if not isinstance(text, str):      # missing values arrive as NaN
        return None
    match = re.search(r"\d[\d,]*(?:\.\d+)?|\.\d+", text)
    if not match:
        return None
    return float(match.group().replace(",", ""))


df = pd.DataFrame({"price_text": raw})
df["price"] = df["price_text"].apply(to_price)
print(df.to_string())
print(df["price"].sum())
