import pandas as pd

path = "output/ch19/files/market_report_q4_2026.xlsx"
sheets = pd.read_excel(path, sheet_name=None, header=None)
for name, sheet in sheets.items():
    print(f"--- {name}: {sheet.shape}")
    print(sheet.head(6).to_string())
