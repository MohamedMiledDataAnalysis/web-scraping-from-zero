import pandas as pd

assets = pd.read_csv("output/ch19/files/eligible_assets.txt",
                     encoding="utf-16", sep="\t", parse_dates=["Maturity"])
print(assets["Currency"].value_counts().to_string())
print("Latest maturity:", assets["Maturity"].max().date())
