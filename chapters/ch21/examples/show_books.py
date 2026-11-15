import pandas as pd

books = pd.read_csv("output/ch21/books.csv")
print(books.shape)
print(books["category"].value_counts().head(3).to_string())
print("Total stock:", books["stock"].sum())
