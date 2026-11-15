from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

folder = Path("output/ch26")
data = pd.read_csv(folder / "dataset/library_value.csv")
by_cat = (data.groupby("category")["pages_per_pound"]
          .agg(books="count", median="median").round(1)
          .sort_values("median", ascending=False))
best, worst = by_cat.index[0], by_cat.index[-1]

fig, ax = plt.subplots(figsize=(6, 4))
ax.barh(by_cat.index[::-1], by_cat["median"][::-1], color="dimgray")
ax.set_xlabel("median pages per pound")
ax.set_title("Pages per pound by category (books in stock)")
fig.tight_layout()
fig.savefig(folder / "pages_per_pound.png", dpi=200)

report = f"""# Which category gives the most pages per pound?

**Answer.** {best}: a median of {by_cat.loc[best, 'median']} pages per pound,
against {by_cat.loc[worst, 'median']} for {worst}, the lowest.

| Category | Books | Median pages per pound |
|---|---|---|
""" + "\n".join(f"| {c} | {r.books} | {r.median} |" for c, r in by_cat.head(5).iterrows()) + f"""

![Pages per pound by category](pages_per_pound.png)

**Method.** {len(data)} books in stock, collected from the library's detail pages on
2027-03-01 (1,050 requests, 0.2 s apart). Pages per pound = pages / price. Median per category.

**Limits.** Prices of one day; out-of-stock books excluded; invented data.
"""
(folder / "report.md").write_text(report, encoding="utf-8")
print(report.split("\n\n")[1].replace("\n", " "))
print(by_cat.head(3).to_string())
