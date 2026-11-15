"""Compare the four methods: cost, fields, agreement."""

import json
from pathlib import Path

import pandas as pd

OUT = Path("output/ch23")
methods = {
    "1 list pages": "m1_list_pages",
    "2 detail pages": "m2_detail_pages",
    "3 Playwright": "m3_playwright",
    "4 Scrapy": "m4_scrapy",
}
rows = []
frames = {}
for label, name in methods.items():
    df = pd.read_csv(OUT / f"{name}.csv")
    frames[label] = df
    sent = json.loads(
        (OUT / f"{name.split('_')[0]}_meta.json").read_text()
    )["requests"]
    rows.append(
        {
            "method": label,
            "books": len(df),
            "columns": len(df.columns),
            "requests": sent,
            "minimum time (s)": round(sent * 0.2),
        }
    )
print(pd.DataFrame(rows).to_string(index=False))

base = frames["2 detail pages"].set_index("title")["price"]
for label, df in frames.items():
    other = df.set_index("title")["price"]
    common = base.index.intersection(other.index)
    differ = (base[common] - other[common]).abs().gt(0.001).sum()
    print(
        f"{label:<15} same titles: {len(common)}, "
        f"price differences: {differ}"
    )
