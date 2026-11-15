import pandas as pd

s = pd.Series(
    ["  In stock\n", "IN STOCK", "In\xa0stock", "Out of  stock "]
)
print(s.tolist())
clean = (
    s.str.replace("\xa0", " ")
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
    .str.lower()
)
print(clean.tolist())
print(clean.value_counts().to_string())
