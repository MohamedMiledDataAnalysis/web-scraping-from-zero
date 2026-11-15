import pandas as pd

books = pd.read_excel("output/ch23/catalogue.xlsx", sheet_name="Catalogue")
counts = books["title"].value_counts()
shared = counts[counts > 1]
print(len(shared), "shared titles")
if len(shared):
    print(shared.index[0], shared.iloc[0])
