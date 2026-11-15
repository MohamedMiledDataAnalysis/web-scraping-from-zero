import pandas as pd

issuance = pd.read_excel("output/ch19/files/market_report_q4_2026.xlsx",
                         sheet_name="Issuance", header=3)
countries = issuance.dropna(subset=["Q1 2026"])
countries = countries[countries["Country"] != "Total"]
print(countries.drop(columns="Country").sum().round(1).to_string())
