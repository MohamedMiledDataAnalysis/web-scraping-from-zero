import pandas as pd

summary = pd.read_excel("output/ch23/catalogue.xlsx", sheet_name="Summary")
print(summary.nlargest(3, "avg_price")[["category", "avg_price"]].to_string(index=False))
