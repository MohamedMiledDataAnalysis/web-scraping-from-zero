import pandas as pd

data = pd.read_csv("output/ch26/dataset/library_value.csv")
data["period"] = pd.cut(data["year"], bins=[1900, 1989, 2009, 2100],
                        labels=["before 1990", "1990-2009", "2010 on"])
print(data.groupby("period", observed=True)["pages_per_pound"]
          .agg(["count", "median"]).round(1).to_string())
