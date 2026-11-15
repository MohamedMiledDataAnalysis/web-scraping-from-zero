import pandas as pd

url = "http://localhost:8000/files/bank_capital_eu.csv"
wrong = pd.read_csv(url)
print(wrong.shape, list(wrong.columns)[:1])

banks = pd.read_csv(url, sep=";", decimal=",", thousands=".")
print(banks.shape)
print(banks.dtypes.to_string())
adverse = banks[(banks["Scenario"] == "Adverse") & (banks["Year"] == 2025)]
print(adverse[["Bank", "CET1 ratio (%)"]].sort_values("CET1 ratio (%)").to_string(index=False))
