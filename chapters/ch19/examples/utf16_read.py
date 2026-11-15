import pandas as pd

raw = open("output/ch19/files/eligible_assets.txt", "rb").read(12)
print(raw)
assets = pd.read_csv("output/ch19/files/eligible_assets.txt",
                     encoding="utf-16", sep="\t")
print(assets.shape)
print(assets.head(3).to_string(index=False))
print(assets.groupby("Asset type")["Haircut (%)"].mean().round(2).to_string())
