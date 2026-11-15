"""Build the downloadable files of the Files section (site/files).

Every figure is invented. The layouts copy the traps of real public files:
semicolons and decimal commas, UTF-16 text, Excel workbooks with title rows
and notes, and a table inside a PDF.
Run:  python site/generate_files.py
"""
import csv
import datetime as dt
import random
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font
from reportlab import rl_config
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

rl_config.invariant = 1          # same bytes on every run
OUT = Path(__file__).parent / "files"
OUT.mkdir(exist_ok=True)
rng = random.Random(42)

# 1. A clean CSV ------------------------------------------------------------
with open(OUT / "monthly_sales.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["month", "region", "units", "revenue_gbp"])
    for m in range(1, 13):
        for region in ["North", "South", "East", "West"]:
            units = rng.randint(80, 400)
            w.writerow([f"2026-{m:02d}", region, units, round(units * rng.uniform(18, 26), 2)])

# 2. A European CSV: semicolons, decimal commas, thousands dots --------------
banks = [("Banque Lumière", "FR", "969500PGLUMIERE00001"),
         ("Nordhafen Bank", "DE", "529900PGNORDHAFEN002"),
         ("Banco Brisa", "ES", "959800PGBRISA0000003"),
         ("Kanaal Bank", "NL", "724500PGKANAAL000004"),
         ("Banca Collina", "IT", "815600PGCOLLINA00005"),
         ("Northbridge Bank", "UK", "213800PGNORTHBRIDGE6")]
with open(OUT / "bank_capital_eu.csv", "w", newline="", encoding="utf-8") as f:
    f.write("LEI;Bank;Country;Year;Total assets (EUR m);CET1 ratio (%);Scenario\n")
    for name, country, lei in banks:
        assets = rng.uniform(80_000, 1_400_000)
        for year in (2024, 2025):
            for scen, shift in (("Baseline", 0), ("Adverse", -3.6)):
                cet1 = rng.uniform(13, 17.5) + shift
                a = f"{assets:,.1f}".replace(",", " ").replace(".", ",").replace(" ", ".")
                c = f"{cet1:.2f}".replace(".", ",")
                f.write(f"{lei};{name};{country};{year};{a};{c};{scen}\n")

# 3. A UTF-16 tab-separated file (like some central bank lists) --------------
lines = ["ISIN\tIssuer\tAsset type\tCurrency\tHaircut (%)\tMaturity"]
types = ["Covered bond", "ABS", "Government bond", "Corporate bond"]
for i in range(1, 41):
    isin = f"PG{rng.randint(10**9, 10**10 - 1)}{i % 10}"
    lines.append("\t".join([isin, f"Issuer {chr(64 + (i % 26) + 1)} SA",
                            rng.choice(types), rng.choice(["EUR", "EUR", "EUR", "GBP"]),
                            f"{rng.choice([0.5, 1, 1.5, 2.5, 4, 6.5, 9])}",
                            f"20{rng.randint(28, 45)}-{rng.randint(1, 12):02d}-15"]))
(OUT / "eligible_assets.txt").write_text("\r\n".join(lines) + "\r\n", encoding="utf-16")

# 4. A messy Excel market report --------------------------------------------
wb = Workbook()
ws = wb.active
ws.title = "Contents"
ws["A1"] = "Securitisation Market Report, Q4 2026 (invented data)"
ws["A1"].font = Font(bold=True, size=14)
ws["A3"] = "Sheet 'Issuance': new issuance by country (EUR billion)"
ws["A4"] = "Sheet 'Outstanding': outstanding by asset class (EUR billion)"
ws2 = wb.create_sheet("Issuance")
ws2["A1"] = "Table 1. New issuance by country, EUR billion"
ws2["A1"].font = Font(bold=True)
ws2["A2"] = "Source: Practice Ground research (invented)"
ws2.append([])
ws2.append(["Country", "Q1 2026", "Q2 2026", "Q3 2026", "Q4 2026", "Total 2026"])
countries = ["France", "Germany", "Italy", "Netherlands", "Spain", "United Kingdom"]
for c in countries:
    q = [round(rng.uniform(2, 25), 1) for _ in range(4)]
    ws2.append([c] + q + [round(sum(q), 1)])
ws2.append(["Total"] + [f"=SUM({col}5:{col}10)" for col in "BCDEF"])
ws2.append([])
ws2.append(["Note: figures revised since the previous report. Spain Q4 is provisional (p)."])
ws3 = wb.create_sheet("Outstanding")
ws3.append(["Asset class", "2025", "2026"])
for a in ["RMBS", "Auto ABS", "Consumer ABS", "CLO", "CMBS", "SME"]:
    ws3.append([a, round(rng.uniform(20, 600), 1), round(rng.uniform(20, 600), 1)])
FIXED = dt.datetime(2027, 1, 15, 9, 0)
wb.properties.created = wb.properties.modified = FIXED
wb.save(OUT / "market_report_q4_2026.xlsx")

# 5. A cover pool file in a template-like layout ------------------------------
wb = Workbook()
ws = wb.active
ws.title = "B1. Cover pool"
ws.append(["Harmonised-style cover pool report (synthetic example)"])
ws.append(["Issuer", "Banque Lumière SFH (invented)"])
ws.append(["Reporting date", "2026-12-31"])
ws.append([])
ws.append(["Field", "Description", "Value"])
fields = [("M.1.1", "Cover pool size (EUR m)", 12450.6),
          ("M.1.2", "Outstanding covered bonds (EUR m)", 9875.0),
          ("M.1.3", "Overcollateralisation (%)", None),
          ("M.2.1", "Number of loans", 98214),
          ("M.2.2", "Weighted average LTV (%)", 61.4),
          ("M.2.3", "Weighted average seasoning (months)", 58)]
for code, desc, val in fields:
    ws.append([code, desc, val])
ws["C8"] = "=ROUND((C6/C7-1)*100,1)"
wb.properties.created = wb.properties.modified = FIXED
wb.save(OUT / "cover_pool_synthetic.xlsx")

# 6. A PDF with a table -------------------------------------------------------
doc = SimpleDocTemplate(str(OUT / "arrears_report_2026.pdf"), pagesize=A4)
styles = getSampleStyleSheet()
rows = [["Quarter", "Loans in arrears", "Of which 2.5%+ of balance", "Possessions"]]
for q in ["Q1 2026", "Q2 2026", "Q3 2026", "Q4 2026"]:
    total = rng.randint(80_000, 99_000)
    rows.append([q, f"{total:,}", f"{int(total * rng.uniform(.38, .44)):,}",
                 f"{rng.randint(900, 1400):,}"])
t = Table(rows)
t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f3a5f")),
                       ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                       ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                       ("ALIGN", (1, 1), (-1, -1), "RIGHT")]))
doc.build([Paragraph("Mortgage arrears and possessions, 2026", styles["Title"]),
           Paragraph("Invented figures for the Practice Ground website.", styles["Normal"]),
           Spacer(1, 12), t, Spacer(1, 12),
           Paragraph("Note: a loan is in arrears when at least one payment is missed.",
                     styles["Normal"])])
print(sorted(p.name for p in OUT.iterdir()))
