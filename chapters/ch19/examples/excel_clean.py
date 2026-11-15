import pandas as pd

path = "output/ch19/files/market_report_q4_2026.xlsx"
issuance = pd.read_excel(path, sheet_name="Issuance", header=3)
print(issuance.tail(3).to_string())

issuance = issuance.dropna(subset=["Q1 2026"])
issuance = issuance[issuance["Country"] != "Total"]
print(issuance.to_string(index=False))
print("Total 2026:", round(issuance["Total 2026"].sum(), 1))
