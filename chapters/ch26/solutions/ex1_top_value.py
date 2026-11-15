import pandas as pd

data = pd.read_csv("output/ch26/dataset/library_value.csv")
top = data.nlargest(3, "pages_per_pound")[["title", "category", "pages_per_pound"]]
print(top.to_string(index=False))
