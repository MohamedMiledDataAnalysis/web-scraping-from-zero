# Chapter 25 — detailed solutions

These are the solutions printed in the book, word for word: what the question asks, the plan, the code, line by line, reading the result, checking, the mistakes the exercise provokes, the choice it makes, another way to solve it, a variation to try, and what to do if your output differs. Here, each program is followed by its exact output.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 25.1 (easy)

> Print, for each watched product, its lowest price over the two weeks and the day it happened. Expected output:

**What the question asks.** For each of the five watched products, find the lowest price of the two weeks and the day it occurred: two values that belong to the same row.

**The plan.** Read the watched products' history; for each product, find the **row** with the lowest price, not only the lowest value; print the name, price and day of those rows.

```python
import sqlite3

import pandas as pd

with sqlite3.connect("output/ch25/prices.db") as db:
    hist = pd.read_sql(
        "SELECT * FROM prices WHERE id IN (3, 7, 9, 14, 19) ORDER BY day",
        db,
    )
lowest = hist.loc[
    hist.groupby("name")["price"].idxmin(), ["name", "price", "day"]
]
print(lowest.sort_values("name").to_string(index=False))
```

Output:

```text
                       name  price        day
            27-inch Monitor 329.19 2027-03-13
                  Air Fryer  30.17 2027-03-03
Noise-Cancelling Headphones 100.85 2027-03-02
             Office Printer  19.90 2027-03-14
                Smart Watch 315.89 2027-03-02
```

**Line by line.**

- `WHERE id IN (3, 7, 9, 14, 19)` keeps the five watched products: 70 rows, 14 days each.
- `hist.groupby("name")["price"].idxmin()` returns, for each product, the row label of its lowest price.
- `hist.loc[labels, ["name", "price", "day"]]` takes those five rows and three columns.
- `sort_values("name")` lists the products in alphabetical order.

**Reading the result.** Each product reached its lowest price on a different day: the headphones and the smart watch early (2 March), the printer and the monitor late (13 and 14 March).

**Checking.** Each lowest price occurs only once in its product's history (count the rows equal to the minimum: 1 for each), so there is no tie to choose between. Sorting by name, price and day and keeping the first row per name gives the same five rows.

**Mistakes this exercise provokes.**

- `hist.groupby("name")["price"].min()`: the right prices but no days, because the minimum is a value, not a row.
- `hist.groupby("name").min()`: the minimum of **each column separately**, so the `day` shown is the first day, 2027-03-01, not the day of the low price.
- `idxmin` on a table whose index has repeated labels: `.loc` then returns several rows per label. `read_sql` gives a clean 0, 1, 2… index.

**The choice it makes.** `groupby("name")["price"].idxmin()` gives, for each product, the row label of its lowest price; `.loc[...]` takes those rows with all their columns. When two days tie, `idxmin` keeps the first; say so if ties are possible.

**Another way to solve it.** Sort and keep the first row of each product:

```python
lowest = (hist.sort_values(["name", "price", "day"])
          .drop_duplicates("name")[["name", "price", "day"]])
```

The same five rows. Sorting by `day` as well makes the tie rule explicit: the earliest day wins.

The same question in SQL, with a sub-query that finds each minimum:

```sql
SELECT name, price, MIN(day) AS day FROM prices p
WHERE id IN (3, 7, 9, 14, 19)
  AND price = (SELECT MIN(price) FROM prices WHERE id = p.id)
GROUP BY name, price ORDER BY name
```

**A variation to try.** Add the highest price and its day beside the lowest, with `idxmax`, and compute how much a buyer saved by buying on the best day rather than the worst.

**If your output differs.**

1. **Every day is 2027-03-01**: you used `groupby("name").min()`.
2. **Fewer than five rows**: the history does not cover the two weeks; run the chapter's `two_weeks.py`.

---

## Exercise 25.2 (medium)

> Which product of the whole Price Watch (not only the watch list) had the largest gap between its highest and lowest price over the two weeks, in per cent of its lowest price? Expected output:

**What the question asks.** Measure each product's price swing over the two weeks, as a percentage of its lowest price, across all 20 products, and name the most volatile.

**The plan.** Group by product, take the minimum and the maximum, compute `max / min − 1` in per cent, sort, keep the top row.

```python
import sqlite3

import pandas as pd

with sqlite3.connect("output/ch25/prices.db") as db:
    hist = pd.read_sql("SELECT name, price FROM prices", db)
spread = hist.groupby("name")["price"].agg(["min", "max"])
spread["gap_pct"] = ((spread["max"] / spread["min"] - 1) * 100).round(1)
print(spread.sort_values("gap_pct", ascending=False).head(1).to_string())
```

Output:

```text
             min   max  gap_pct
name                           
Air Fryer  30.17  40.2     33.2
```

**Line by line.**

- `SELECT name, price FROM prices` reads all 280 rows: 20 products, 14 days.
- `.agg(["min", "max"])` computes both statistics per product, in two columns.
- `spread["max"] / spread["min"] - 1` is the rise from the lowest to the highest price, as a fraction; `* 100` turns it into per cent; `.round(1)` keeps one decimal.
- `sort_values("gap_pct", ascending=False).head(1)` keeps the largest gap.

**Reading the result.** The Air Fryer moved between £30.17 and £40.20: its highest price was 33.2% above its lowest. A buyer who picked the wrong day paid a third more.

**Checking.** The next products are the Noise-Cancelling Headphones (27.8%) and the Action Camera (26.4%): print `.head(3)` to see them. Recompute the top one: 40.20 / 30.17 = 1.332.

**Mistakes this exercise provokes.**

- Dividing by the maximum (`1 - min / max`): 25.0% for the Air Fryer, a different measure. Both are valid; say which one you use.
- Comparing the gaps in pounds: the Smart Watch moves by more pounds than the Air Fryer simply because it costs ten times more.
- Reading only the watched products: the question asks for all 20.

**The choice it makes.** The monitor stores all 20 products, not only the watched ones: the history costs nothing more (it is the same request), and questions like this one become possible later. The max-to-min gap reacts to one unusual day; a standard deviation of daily changes measures the usual movement instead.

**Another way to solve it.** Let SQLite compute it:

```python
query = """
    SELECT name, MIN(price) AS min, MAX(price) AS max,
           ROUND((MAX(price) / MIN(price) - 1) * 100, 1) AS gap_pct
    FROM prices GROUP BY name ORDER BY gap_pct DESC LIMIT 1
"""
```

The same row. The database sends back one row instead of 280.

**A variation to try.** Measure day-to-day movement instead of the extreme gap: for each product, `hist.sort_values("day").groupby("name")["price"].pct_change().abs()`, then average it per product. Compare the ranking with the gap ranking: a product with one sale day ranks high on the gap and low on daily movement.

**If your output differs.**

1. **A product with a gap of 0**: the history has one day only for it; check the number of rows per product.
2. **`inf` in `gap_pct`**: a price of 0 is stored, and dividing by it gives infinity; `run_day` refuses prices of 0 or less, so the row came from other code.

---

## Exercise 25.3 (medium)

> Run the alerts of 2027-03-10 again with a target 5% higher for every product, without collecting again (`alerts_for` reads the database only). Expected output:

**What the question asks.** Test how sensitive the alerts are to the targets: raise every target by 5% and re-run the alert check of 10 March on the stored history, without any new request.

**The plan.** Read the watch list, multiply the `target` column by 1.05, round to pence, pass the modified table to `alerts_for`, print the messages or `No alert`.

```python
import sys

import pandas as pd

sys.path.insert(0, "chapters/ch25/project")
from monitor import alerts_for  # noqa: E402

watch = pd.read_csv("output/ch25/watchlist.csv")
watch["target"] = (watch["target"] * 1.05).round(2)
for message in alerts_for("2027-03-10", watch) or ["No alert"]:
    print(message)
```

Output:

```text
27-inch Monitor: £335.64, at or below your target £346.50
Office Printer: £19.98, at or below your target £20.95
```

**Line by line.**

- `pd.read_csv("output/ch25/watchlist.csv")` reads the five products and their targets.
- `watch["target"] * 1.05` raises every target by 5%; `.round(2)` keeps pence, so that £330.00 becomes £346.50.
- `alerts_for("2027-03-10", watch)` reads the history up to that day from the database and returns a list of messages; it sends no request.
- `alerts_for(...) or ["No alert"]` gives the list when it is not empty, and the one-message list otherwise; the loop prints each.

**Reading the result.** Two alerts: the 27-inch Monitor at £335.64 is now under its raised target of £346.50, and the Office Printer at £19.98 is under £20.95. With the original targets (£330.00 and £19.95), neither price qualified: on 10 March, `alerts_for` with the original list returns an empty list.

**Checking.** Compare the other three: the Smart Watch costs £347.24 against a raised target of £331.80, the Headphones £126.04 against £105.00, the Air Fryer £38.77 against £32.02. None is near.

**Mistakes this exercise provokes.**

- Changing `watchlist.csv` itself: the next real run would use the raised targets. Change a copy in memory.
- `watch["target"] + 5`: five pounds, not five per cent.
- Calling `run_day` instead of `alerts_for`: it collects the day again, which the exercise forbids.

**The choice it makes.** `list or ["No alert"]` gives the list when it is not empty, and the one-message list otherwise. Keeping collection (`run_day`) separate from analysis (`alerts_for`) is what makes this test free: you can try a hundred settings on stored data without sending a single request.

**Another way to solve it.** Find, for each product, how high the target would have to be for an alert on 10 March: it is simply that day's price. Compare it with the current target:

```python
import sqlite3

with sqlite3.connect("output/ch25/prices.db") as db:
    today = pd.read_sql("SELECT id, price FROM prices WHERE day = '2027-03-10'", db)
gap = watch.merge(today, on="id")
gap["raise_needed_pct"] = ((gap["price"] / gap["target"] - 1) * 100).round(1)
```

With the original targets, the monitor needs a raise of 1.7% and the printer of 0.2%, the other three far more. This tells you the threshold directly instead of trying values.

**A variation to try.** Loop over raises of 0%, 2%, 5% and 10% and print the number of alerts for each. Then run the same loop over every day of the two weeks: a target that alerts every day is too high to be useful.

**If your output differs.**

1. **`No alert`**: the targets were not raised; print `watch`.
2. **`£20.95` shown as `£20.94`**: rounding of `19.95 × 1.05 = 20.9475`; `.round(2)` gives 20.95 here, but a target computed differently can round the other way. Store targets in pence when exactness matters.

---

## Exercise 25.4 (harder)

> Draw one chart with the five watched products, each line divided by its own first price (so they all start at 1.0), and print which product ended the two weeks with the largest fall. Save it as `output/ch25/watchlist_index.png`. Expected output:

**What the question asks.** Compare five products whose prices differ by a factor of twenty on one chart, by dividing each line by its own first price; then name the product whose price fell most over the two weeks.

**The plan.** Read the history with real dates; turn it into one column per product with `pivot`; divide by the first row; draw the five lines in black with different line styles; save the figure; compute the final change of each product.

```python
import sqlite3

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

with sqlite3.connect("output/ch25/prices.db") as db:
    hist = pd.read_sql(
        "SELECT day, name, price FROM prices "
        "WHERE id IN (3, 7, 9, 14, 19)",
        db,
        parse_dates=["day"],
    )
table = hist.pivot(index="day", columns="name", values="price")
index = table / table.iloc[0]
fig, ax = plt.subplots(figsize=(6, 3.5))
for i, name in enumerate(index.columns):
    ax.plot(
        index.index,
        index[name],
        label=name,
        color="black",
        linestyle=["-", "--", ":", "-.", (0, (1, 3))][i],
    )
ax.axhline(1.0, color="grey", linewidth=0.5)
ax.legend(fontsize=7)
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig("output/ch25/watchlist_index.png", dpi=200)
change = (index.iloc[-1] - 1) * 100
print(f"Largest fall: {change.idxmin()} ({change.min():.1f}%)")
```

Output:

```text
Largest fall: 27-inch Monitor (-8.4%)
```

**Line by line.**

- `matplotlib.use("Agg")` draws without a window, which works on any computer.
- `parse_dates=["day"]` turns the text dates into real dates, so the axis is spaced correctly.
- `hist.pivot(index="day", columns="name", values="price")` makes one row per day and one column per product.
- `table / table.iloc[0]` divides every row by the first row: each column now starts at 1.0.
- The loop draws one line per product, all black, with a line style chosen by position.
- `ax.axhline(1.0, ...)` draws the starting level, so rises and falls are visible at a glance.
- `fig.autofmt_xdate()` tilts the dates so they do not overlap.
- `change = (index.iloc[-1] - 1) * 100` is each product's change from the first to the last day, in per cent; `idxmin()` names the smallest, the largest fall.

**Reading the result.** The 27-inch Monitor fell most: 8.4% below its 1 March price on 14 March. Only one other product ended lower than it started, the Office Printer (−0.5%); the Air Fryer rose 31.2%.

**Checking.** Print `change.round(1)`: −8.4 for the monitor, −0.5 for the printer, +9.0 for the smart watch, +25.1 for the headphones, +31.2 for the air fryer. Open the PNG: the monitor's line ends lowest.

**Mistakes this exercise provokes.**

- Plotting raw prices: the £30 air fryer is a flat line at the bottom, under the £330 monitor and smart watch.
- Dividing by the **mean** instead of the first price: the lines no longer start together, and *fall over the two weeks* loses its meaning.
- Text dates on the axis: fourteen labels in alphabetical order, which happens to be correct here but breaks with other formats.

**The choice it makes.** `pivot` turns the long table (one row per product per day) into a wide one (one column per product). Dividing by the first row puts every product on the same scale. Line styles instead of colours keep the chart readable in a black-and-white book. The index answers *by how much did it change?*; it hides *how much does it cost?*, so give the prices in a table beside it.

**Another way to solve it.** pandas draws all the columns at once:

```python
ax = index.plot(figsize=(6, 3.5), style=["-", "--", ":", "-.", "-"], color="black")
ax.axhline(1.0, color="grey", linewidth=0.5)
ax.figure.savefig("output/ch25/watchlist_index.png", dpi=200, bbox_inches="tight")
```

Shorter; the explicit loop gives you full control over each line, such as the dotted style `(0, (1, 3))` that `style` cannot express.

**A variation to try.** Label each line at its right end instead of using a legend: after the loop, `ax.text(index.index[-1], index[name].iloc[-1], name, fontsize=7)` for each product. Direct labels are easier to read than a legend when lines cross.

**If your output differs.**

1. **`ValueError: Index contains duplicate entries, cannot reshape`**: a product has two rows for one day; the backfill example of the chapter wrote into the main database. Check with `hist.duplicated(["day", "name"]).sum()`.
2. **Lines that do not start at 1.0**: the table is not sorted by day before `iloc[0]`; `pivot` sorts its index, so check that `day` was parsed as a date.
