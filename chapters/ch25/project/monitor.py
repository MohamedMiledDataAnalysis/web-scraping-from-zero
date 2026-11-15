"""Daily price monitor: one request, history in SQLite, two kinds of alert."""
import sqlite3
import sys
from io import StringIO

import pandas as pd

sys.path.insert(0, ".")
from toolkit.polite import PoliteClient  # noqa: E402

DB = "output/ch25/prices.db"
client = PoliteClient("PriceMonitor/1.0 (+mailto:reader@example.com)", delay=0.2)


def read_prices(day):
    """Every product's price on `day`, from the Price Watch table."""
    html = client.get(f"http://localhost:8000/prices/?day={day}").text
    table = pd.read_html(StringIO(html), attrs={"id": "prices"})[0]
    ids = pd.read_html(StringIO(html), attrs={"id": "prices"}, extract_links="body")[0]
    table["id"] = ids["Product"].map(lambda cell: int(cell[1].strip("/").split("/")[-1]))
    table["price"] = table["Price"].str.lstrip("£").astype(float)
    return table[["id", "Product", "price"]].rename(columns={"Product": "name"})


def store(day, prices):
    with sqlite3.connect(DB) as db:
        db.execute("CREATE TABLE IF NOT EXISTS prices (day TEXT, id INTEGER, "
                   "name TEXT, price REAL, PRIMARY KEY (day, id))")
        db.execute("DELETE FROM prices WHERE day = ?", (day,))
        prices.assign(day=day).to_sql("prices", db, if_exists="append", index=False)


def alerts_for(day, watch):
    """Target reached, or a drop of 10% or more below the previous 7 days' average."""
    with sqlite3.connect(DB) as db:
        hist = pd.read_sql("SELECT * FROM prices WHERE day <= ?", db, params=(day,))
    out = []
    for w in watch.itertuples():
        mine = hist[hist["id"] == w.id].sort_values("day")
        today = mine[mine["day"] == day]
        if today.empty:
            continue
        price = today["price"].iloc[0]
        before = mine[mine["day"] < day].tail(7)["price"]
        if price <= w.target:
            out.append(f"{w.name}: £{price:.2f}, at or below your target £{w.target:.2f}")
        elif len(before) >= 3 and price <= 0.9 * before.mean():
            out.append(f"{w.name}: £{price:.2f}, {1 - price / before.mean():.0%} "
                       f"below its 7-day average £{before.mean():.2f}")
    return out


def run_day(day, watch):
    prices = read_prices(day)
    if len(prices) != 20 or prices["price"].le(0).any():
        raise RuntimeError(f"check failed on {day}")
    store(day, prices)
    return alerts_for(day, watch)
