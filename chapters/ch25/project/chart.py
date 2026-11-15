import sqlite3

import matplotlib
import pandas as pd

matplotlib.use("Agg")                       # draw to a file, no window
import matplotlib.pyplot as plt  # noqa: E402

product_id, target = 9, 316.00
with sqlite3.connect("output/ch25/prices.db") as db:
    hist = pd.read_sql("SELECT day, price, name FROM prices WHERE id = ? ORDER BY day",
                       db, params=(product_id,), parse_dates=["day"])

fig, ax = plt.subplots(figsize=(6, 3))
ax.plot(hist["day"], hist["price"], marker="o", color="black", label="price")
ax.axhline(target, linestyle="--", color="grey", label=f"target £{target:.0f}")
ax.set_title(f"{hist['name'].iloc[0]}: daily price")
ax.set_ylabel("£")
ax.legend()
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig("output/ch25/smart_watch.png", dpi=200)
print("Lowest:", hist["price"].min(), "on", hist.loc[hist["price"].idxmin(), "day"].date())
print("Days at or below target:", int((hist["price"] <= target).sum()))
