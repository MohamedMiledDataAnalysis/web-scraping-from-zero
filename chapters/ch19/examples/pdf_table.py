import pandas as pd
import pdfplumber

path = "output/ch19/files/arrears_report_2026.pdf"
with pdfplumber.open(path) as pdf:
    print(len(pdf.pages), "page(s)")
    page = pdf.pages[0]
    print(page.extract_text().splitlines()[0])
    rows = page.extract_table()

print(rows[:2])
table = pd.DataFrame(rows[1:], columns=rows[0])
for col in table.columns[1:]:
    table[col] = table[col].str.replace(",", "").astype(int)
print(table.to_string(index=False))
print("Possessions in 2026:", table["Possessions"].sum())
