import pandas as pd

out = pd.read_excel("output/ch19/files/market_report_q4_2026.xlsx",
                    sheet_name="Outstanding")
out["growth"] = out["2026"] - out["2025"]
best = out.loc[out["growth"].idxmax()]
print(best["Asset class"], round(best["growth"], 1))
