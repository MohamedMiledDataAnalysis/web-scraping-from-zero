import pandas as pd

books = pd.read_excel("output/ch23/catalogue.xlsx", sheet_name="Catalogue")
print(books.groupby("rating")["price"].mean().round(2).to_string())
print("Correlation:", round(books["price"].corr(books["rating"]), 3))
