import sqlite3

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

with sqlite3.connect("output/ch25/prices.db") as db:
    hist = pd.read_sql("SELECT day, name, price FROM prices WHERE id IN (3, 7, 9, 14, 19)",
                       db, parse_dates=["day"])
table = hist.pivot(index="day", columns="name", values="price")
index = table / table.iloc[0]
fig, ax = plt.subplots(figsize=(6, 3.5))
for i, name in enumerate(index.columns):
    ax.plot(index.index, index[name], label=name, color="black",
            linestyle=["-", "--", ":", "-.", (0, (1, 3))][i])
ax.axhline(1.0, color="grey", linewidth=0.5)
ax.legend(fontsize=7)
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig("output/ch25/watchlist_index.png", dpi=200)
change = (index.iloc[-1] - 1) * 100
print(f"Largest fall: {change.idxmin()} ({change.min():.1f}%)")
