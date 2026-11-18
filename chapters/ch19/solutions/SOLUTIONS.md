# Chapter 19 — detailed solutions

These are the solutions printed in the book, word for word: what the question asks, the plan, the code, line by line, reading the result, checking, the mistakes the exercise provokes, the choice it makes, another way to solve it, a variation to try, and what to do if your output differs. Here, each program is followed by its exact output.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 19.1 (easy)

> Download `monthly_sales.csv` with streaming, check that its `Content-Type` is `text/csv`, and print the best month for the *North* region. Expected output:

**What the question asks.** Download a file the way you would download a large one (in pieces, with `stream=True`), check that it really is a CSV before trusting it, then answer a question: the best month of the *North* region.

**The plan.** Open the request with `stream=True` inside a `with` block; check the status and the `Content-Type`; write the file chunk by chunk; read it with pandas; filter and find the maximum.

```python
from pathlib import Path

import pandas as pd
import requests

path = Path("output/ch19/monthly_sales.csv")
path.parent.mkdir(parents=True, exist_ok=True)
with requests.get(
    "http://localhost:8000/files/monthly_sales.csv",
    stream=True,
    timeout=60,
) as r:
    r.raise_for_status()
    assert r.headers["Content-Type"].startswith("text/csv"), r.headers[
        "Content-Type"
    ]
    with open(path, "wb") as f:
        for chunk in r.iter_content(65536):
            f.write(chunk)
sales = pd.read_csv(path)
north = sales[sales["region"] == "North"]
best = north.loc[north["revenue_gbp"].idxmax()]
print(best["month"], best["revenue_gbp"])
```

Output:

```text
2026-03 7666.86
```

**Line by line.**

- `stream=True` tells `requests` not to load the whole file into memory at once.
- `with requests.get(...) as r:` closes the connection at the end of the block, even after an error.
- `assert r.headers["Content-Type"].startswith("text/csv"), ...` stops the program with the actual type if the server sent something else, such as an HTML error page.
- `r.iter_content(65536)` returns the file in pieces of 64 kilobytes; each piece is written to the open file, in binary mode (`"wb"`).
- `sales[sales["region"] == "North"]` keeps the North rows; `idxmax()` and `.loc` give the row with the highest revenue.

**Reading the result.** March 2026, with £7,666.86: North's best month of the year. The file has 48 rows, 12 months for each of four regions.

**Checking.** `print(r.headers["Content-Type"])` shows `text/csv; charset=utf-8`, which is why the test uses `startswith`. The second-best North month is October, with £6,086.73: March leads clearly.

**Mistakes this exercise provokes.**

- `r.headers["Content-Type"] == "text/csv"`: `False`, because of the `; charset=utf-8` part. Use `startswith`.
- Opening the file with `"w"` instead of `"wb"`: `TypeError`, because the chunks are bytes, not text.
- Saving without checking the type: a redirect to an error page would be saved under the name `monthly_sales.csv`.

**The choice it makes.** This file is 1,297 bytes, so streaming changes nothing here; it is the habit that matters for files of hundreds of megabytes. `assert condition, message` stops the program with the message when the condition is false: a one-line guard for a check that must never fail.

**Another way to solve it.** For a small file, read it straight into pandas without saving it:

```python
r = requests.get("http://localhost:8000/files/monthly_sales.csv", timeout=60)
r.raise_for_status()
sales = pd.read_csv(io.StringIO(r.text))
```

It gives the same DataFrame. Save to disk when you want to keep the file or when it is large; read from memory for a quick look.

**A variation to try.** The best month of **every** region in one step:

```python
best = sales.loc[sales.groupby("region")["revenue_gbp"].idxmax(), ["region", "month", "revenue_gbp"]]
print(best.to_string(index=False))
```

```text
region   month  revenue_gbp
  East 2026-12      8188.44
 North 2026-03      7666.86
 South 2026-06      9933.11
  West 2026-12      8121.01
```

**If your output differs.**

1. **`AssertionError: text/html; charset=utf-8`**: the server sent a page, not the file; check the address.
2. **`TypeError: write() argument must be str, not bytes`**: open the file with `"wb"`.

---

## Exercise 19.2 (medium)

> From `eligible_assets.txt`, print the number of assets per currency and the latest maturity date. Expected output:

**What the question asks.** Read the UTF-16, tab-separated file of Chapter 8 correctly, then two facts: the number of assets per currency, and the latest maturity date.

**The plan.** `read_csv` with three settings (the encoding, the separator, and a date column), then `value_counts()` and `max()`.

```python
import pandas as pd

assets = pd.read_csv("output/ch19/files/eligible_assets.txt",
                     encoding="utf-16", sep="\t", parse_dates=["Maturity"])
print(assets["Currency"].value_counts().to_string())
print("Latest maturity:", assets["Maturity"].max().date())
```

Output:

```text
Currency
EUR    31
GBP     9
Latest maturity: 2045-04-15
```

**Line by line.**

- `encoding="utf-16"` decodes the file correctly: the site announces UTF-8, but the file is UTF-16 (Chapter 8).
- `sep="\t"` splits columns at tabs.
- `parse_dates=["Maturity"]` converts that column to dates while reading.
- `assets["Currency"].value_counts()` counts the rows for each currency, most frequent first.
- `assets["Maturity"].max()` is the latest date; `.date()` drops the time part, which is midnight.

**Reading the result.** 40 assets: 31 in euros and 9 in pounds. The longest-dated matures on 15 April 2045.

**Checking.** `print(assets.dtypes)` shows a `datetime64` type for `Maturity` and `float64` for the haircut. `len(assets)` is 40, the count found in Chapter 8.

**Mistakes this exercise provokes.**

- Forgetting `encoding="utf-16"`: `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0`.
- Forgetting `sep="\t"`: one single column holding whole lines.
- Taking the maximum without `parse_dates`: it happens to work here, because ISO dates sort like text, but you cannot calculate with them (add days, subtract dates) until they are dates.

**The choice it makes.** `parse_dates` converts the column at reading time, once. Run `download_all.py` first: this solution reads the downloaded copy in `output/ch19/files/`, so you can run it again without asking the site.

**Another way to solve it.** Convert after reading, with `pd.to_datetime`:

```python
assets = pd.read_csv("output/ch19/files/eligible_assets.txt", encoding="utf-16", sep="\t")
assets["Maturity"] = pd.to_datetime(assets["Maturity"])
```

The same result. Converting afterwards is useful when you must first clean the column, for example to remove notes such as `(p)`.

**A variation to try.** Two more questions, each one line:

```python
print(assets.groupby("Currency")["Haircut (%)"].mean().round(2).to_dict())
print(assets["Asset type"].value_counts().to_dict())
```

The average haircut is 3.92% for euro assets and 2.33% for sterling ones; covered bonds are the most common asset type, with 16.

**If your output differs.**

1. **`FileNotFoundError`**: run `download_all.py` first.
2. **`UnicodeDecodeError`**: add `encoding="utf-16"`.
3. **`KeyError: 'Currency'`**: the separator is wrong; print `assets.columns`.

---

## Exercise 19.3 (medium)

> From the *Outstanding* sheet of the market report, print the asset class with the largest growth between 2025 and 2026, in EUR billion. Expected output:

**What the question asks.** From one sheet of an Excel workbook, the asset class whose outstanding amount grew most between 2025 and 2026, and by how much.

**The plan.** `read_excel` with the sheet's name; subtract the two year columns into a new column; take the row with the largest growth.

```python
import pandas as pd

out = pd.read_excel("output/ch19/files/market_report_q4_2026.xlsx",
                    sheet_name="Outstanding")
out["growth"] = out["2026"] - out["2025"]
best = out.loc[out["growth"].idxmax()]
print(best["Asset class"], round(best["growth"], 1))
```

Output:

```text
Consumer ABS 170.1
```

**Line by line.**

- `sheet_name="Outstanding"` chooses the sheet by its name; without it, pandas reads the first sheet, *Contents*.
- The sheet's header is on the first row, so the default `header=0` is right.
- `out["2026"] - out["2025"]` subtracts the columns row by row; the column names are text.
- `out["growth"].idxmax()` gives the row with the largest growth; `round(..., 1)` keeps one decimal.

**Reading the result.** Consumer ABS grew by €170.1 billion, from 93.8 to 263.9. Three classes shrank: CMBS, CLO and Auto ABS.

**Checking.** `print(out.sort_values("growth"))` lists every class with its change; the last line is Consumer ABS. `list(out.columns)` shows `['Asset class', '2025', '2026']`.

**Mistakes this exercise provokes.**

- `out[2025]` with a number: `KeyError: 2025`, because these column names are text.
- Reading without `sheet_name`: the *Contents* sheet, which has no `2025` column.
- Taking the largest **percentage** growth instead: also Consumer ABS here, but on another sheet the two can differ. The question asks for the amount.

**The choice it makes.** This sheet is clean: header on the first row, no notes. Column names that look like numbers (`2025`) are text here because the workbook stores them as text; a numeric header cell gives an integer column name (`out[2025]`). Check with `list(out.columns)`.

**Another way to solve it.** Rename the columns to avoid the text-or-number question altogether:

```python
out.columns = ["asset_class", "y2025", "y2026"]
out["growth"] = out["y2026"] - out["y2025"]
```

Names that start with a letter and contain no spaces are easier to type and work with `query`.

**A variation to try.** Compute the growth in per cent: `(out["2026"] / out["2025"] - 1) * 100`. Consumer ABS leads again, with 181.3%: its amount almost tripled.

**If your output differs.**

1. **`KeyError: '2025'`**: print `list(out.columns)`; your copy of the file may store the years as numbers.
2. **`ValueError: Worksheet named 'Outstanding' not found`**: check the sheet name with `pd.ExcelFile(path).sheet_names`.

---

## Exercise 19.4 (medium)

> Recompute the *Total* row of the *Issuance* sheet (the sum of each quarter over the six countries), and print it. Expected output:

**What the question asks.** The *Issuance* sheet has a *Total* row whose formulas were not saved with values, so pandas reads it as empty. Recompute it: the sum of each column over the six countries.

**The plan.** Read the sheet with its header on row 4 (`header=3`); keep only the country rows; sum every number column.

```python
import pandas as pd

issuance = pd.read_excel("output/ch19/files/market_report_q4_2026.xlsx",
                         sheet_name="Issuance", header=3)
countries = issuance.dropna(subset=["Q1 2026"])
countries = countries[countries["Country"] != "Total"]
print(countries.drop(columns="Country").sum().round(1).to_string())
```

Output:

```text
Q1 2026        62.3
Q2 2026        87.7
Q3 2026        86.7
Q4 2026        83.7
Total 2026    320.4
```

**Line by line.**

- `header=3` tells pandas that the column names are on the fourth row of the sheet (rows are counted from 0); the three rows above are a title, a source line and a blank.
- `issuance.dropna(subset=["Q1 2026"])` removes the rows with no value in `Q1 2026`: the note, the blank row, and here also the *Total* row.
- `countries[countries["Country"] != "Total"]` removes a *Total* row in case its values were saved.
- `countries.drop(columns="Country")` keeps the number columns; `.sum()` adds each column; `.round(1)` keeps one decimal.

**Reading the result.** Issuance rose from €62.3 billion in Q1 to €87.7 billion in Q2, and reached €320.4 billion for the year.

**Checking.** `countries["Country"].tolist()` lists exactly six countries, France to the United Kingdom. The quarters add up to the year: 62.3 + 87.7 + 86.7 + 83.7 = 320.4.

**Mistakes this exercise provokes.**

- `header=0` (the default): the title becomes the column names, and every row is shifted.
- Summing without removing the *Total* row: if its values had been saved, every total would be doubled.
- `sum()` on the whole DataFrame, `Country` included: pandas glues the country names into one long text, `FranceGermanyItaly...`, and the result becomes a column of mixed types. Drop the text column first.

**The choice it makes.** `dropna` removes the note, the blank row and here also the *Total* row (its formulas have no saved values); the label filter is a safety net for files where the totals were saved. Never keep a total row in your data, or every sum counts twice.

**Another way to solve it.** Read only the six country rows with `nrows`:

```python
countries = pd.read_excel("output/ch19/files/market_report_q4_2026.xlsx",
                          sheet_name="Issuance", header=3, nrows=6)
print(countries.drop(columns="Country").sum().round(1).to_string())
```

It prints the same totals. Shorter, but it depends on the exact number of countries: if a seventh is added, it is silently left out. The book's version adapts.

**A variation to try.** Print each country's share of the year's issuance, in per cent, largest first: `(countries.set_index("Country")["Total 2026"] / 320.4 * 100).round(1).sort_values(ascending=False)`. The Netherlands leads with 69.4 of 320.4.

Read the note under the table too: it says Spain's Q4 figure is provisional. A careful report repeats such notes next to the numbers they concern.

**If your output differs.**

1. **Totals of 0 or `NaN`**: the header row is wrong; print `issuance.head()`.
2. **Doubled totals**: the *Total* row is included.

---

## Exercise 19.5 (harder)

> Write `read_cover_pool(path)` that returns a dictionary with the issuer, the date and every field code. Copy the synthetic file twice under new names with `shutil.copy` (to imitate three issuers' files), read the three, and build a DataFrame with one row per file and the columns `issuer`, `M.1.1`, `M.2.2`. Expected output:

**What the question asks.** A reader for a report format with a small header block (issuer, date) above a table of field codes and values, used on three files, and a comparison table with one row per file.

**The plan.** Copy the synthetic file three times to imitate three issuers. In `read_cover_pool`, read the sheet twice: once without a header to reach the issuer and date cells, once with the header on row 5 for the fields. Combine them into one dictionary per file; build a DataFrame.

```python
import shutil
from pathlib import Path

import pandas as pd

folder = Path("output/ch19/pools")
folder.mkdir(parents=True, exist_ok=True)
source = Path("output/ch19/files/cover_pool_synthetic.xlsx")
for name in ["pool_a.xlsx", "pool_b.xlsx", "pool_c.xlsx"]:
    shutil.copy(source, folder / name)


def read_cover_pool(path):
    raw = pd.read_excel(path, header=None)
    fields = pd.read_excel(path, header=4)
    record = {
        "file": Path(path).name,
        "issuer": raw.iloc[1, 1],
        "date": raw.iloc[2, 1],
    }
    record.update(dict(zip(fields["Field"], fields["Value"])))
    return record


pools = pd.DataFrame(
    [read_cover_pool(p) for p in sorted(folder.glob("*.xlsx"))]
)
print(
    pools[["file", "issuer", "M.1.1", "M.2.2"]].to_string(index=False)
)
```

Output:

```text
       file                        issuer   M.1.1  M.2.2
pool_a.xlsx Banque Lumière SFH (invented) 12450.6   61.4
pool_b.xlsx Banque Lumière SFH (invented) 12450.6   61.4
pool_c.xlsx Banque Lumière SFH (invented) 12450.6   61.4
```

**Line by line.**

- `shutil.copy(source, folder / name)` copies the file under each new name.
- `pd.read_excel(path, header=None)` reads every cell, with numbered columns; `raw.iloc[1, 1]` is the cell at row 1, column 1: the issuer; `raw.iloc[2, 1]` is the date.
- `pd.read_excel(path, header=4)` reads the table whose header (`Field`, `Description`, `Value`) is on row 5.
- `dict(zip(fields["Field"], fields["Value"]))` pairs each code with its value: `{'M.1.1': 12450.6, ...}`.
- `record.update(...)` adds those pairs to the dictionary that already holds `file`, `issuer` and `date`.
- `sorted(folder.glob("*.xlsx"))` lists the files in a fixed order; the list comprehension reads each one.

**Reading the result.** Three rows, identical except for the file name, because the three files are copies: €12,450.6 million of cover pool, and 61.4 for field M.2.2.

**Checking.** `print(raw.head(8))` shows the layout: the title, `Issuer`, `Reporting date`, a blank row, then the table header. Some fields are empty in the file, such as M.1.3; they come back as `NaN`.

**Mistakes this exercise provokes.**

- `header=5` instead of `header=4`: the first field becomes the header and is lost.
- `raw.loc[1, 1]`: works here, because the labels are numbers, but `iloc` states that you mean positions.
- Running the script twice without `exist_ok=True`: `FileExistsError` when creating the folder.

**The choice it makes.** `folder.glob("*.xlsx")` lists the files that match the pattern; `sorted` fixes their order. With real harmonised reports from three issuers, the same function gives a comparison table of their cover pools, one row per issuer and one column per field.

**Another way to solve it.** Read the file once and split it in Python, instead of reading it twice:

```python
raw = pd.read_excel(path, header=None)
table = raw.iloc[5:, [0, 2]]
fields = dict(zip(table[0], table[2]))
```

One read instead of two. It depends on positions (row 5, columns 0 and 2), which is fine for a fixed format and fragile for a changing one.

**A variation to try.** Keep only the fields that have a value in every file, with `pools.dropna(axis=1)`, and transpose the table with `pools.set_index("file").T` so that the fields become rows and the files columns: the layout analysts usually compare.

**If your output differs.**

1. **`KeyError: 'Field'`**: the header row is wrong; print `pd.read_excel(path, header=None).head(8)`.
2. **`FileNotFoundError`**: run `download_all.py` first.
