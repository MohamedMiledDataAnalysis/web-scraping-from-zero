import pandas as pd

banks = pd.read_csv(
    "http://localhost:8000/files/bank_capital_eu.csv",
    sep=";",
    decimal=",",
    thousands=".",
)
adverse = banks[banks["Scenario"] == "Adverse"]
print(
    adverse.groupby("Country")["CET1 ratio (%)"]
    .min()
    .sort_values()
    .to_string()
)
