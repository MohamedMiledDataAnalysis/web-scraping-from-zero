# Chapter 7 — detailed solutions

These are the long versions of the solutions printed in the book. Each has the same parts as the book, with more detail, plus parts the book has no room for: another way to solve the exercise, a variation to try, and what to do if your output differs.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 7.1 (easy)

> Read the planets table and print the names of the planets whose orbital period is longer than 1,000 days. Use `planets[planets["column"] > 1000]`, which keeps the rows where the condition is true. Expected output:

**What the question asks.** From the planets table, the names of the planets whose year lasts more than 1,000 days, as a Python list.

**The plan.** Read the table into a DataFrame with `read_html`, keep the rows that pass the test with a *boolean mask*, then take the `Planet` column as a list.

```python
from io import StringIO

import pandas as pd
import requests

html = requests.get("http://localhost:8000/tables/", timeout=10).text
planets = pd.read_html(StringIO(html), thousands=",")[0]
long_years = planets[planets["Orbital period (days)"] > 1000]
print(long_years["Planet"].tolist())
```

Output:

```text
['Jupiter', 'Saturn', 'Uranus', 'Neptune']
```

**Line by line.**

- `requests.get(...).text` downloads the Tables page; `StringIO(html)` wraps the text so that `read_html` reads it as a file (pandas 3 no longer accepts raw HTML text directly).
- `pd.read_html(..., thousands=",")` returns a **list** of every table on the page; `[0]` takes the first, the planets. `thousands=","` reads `4,331` as 4331.
- `planets["Orbital period (days)"] > 1000` compares every value of the column with 1000 and returns one `True` or `False` per row: a mask.
- `planets[mask]` keeps the rows where the mask is `True`.
- `long_years["Planet"].tolist()` takes the names and turns them into a list.

**Reading the result.** Four planets: Jupiter, Saturn, Uranus and Neptune, the four outer planets. Mars, at 687 days, is just under the line.

**Checking.** `print(planets.dtypes)` shows `float64` for the orbital period: pandas read it as a number, so `>` compares numbers. `print(planets[["Planet", "Orbital period (days)"]])` shows all eight values to compare by eye.

**Mistakes this exercise provokes.**

- A column name with a typo, such as `"Orbital period"`: `KeyError`. Copy names from `print(planets.columns)`.
- `pd.read_html(html)` without `StringIO`: pandas 3 takes the text for a file name and stops with `FileNotFoundError`.
- A column read as text (for example a European table, where `1.432,0` stays text without `decimal=","`): the comparison stops with `TypeError: '>' not supported between instances of 'str' and 'int'`. Always look at `.dtypes` before you calculate.
- `planets["Orbital period (days)" > 1000]`, with the bracket in the wrong place: Python compares the text with 1000 and stops with `TypeError`.

**The choice it makes.** The mask is the standard way to filter in pandas: it states the condition once and works on any number of rows.

### Another way to solve it

`.loc[rows, column]` filters and selects in one step:

```python
print(planets.loc[planets["Orbital period (days)"] > 1000, "Planet"].tolist())
```

`query` writes the condition as text; column names with spaces go between backticks:

```python
print(planets.query("`Orbital period (days)` > 1000")["Planet"].tolist())
```

Both print `['Jupiter', 'Saturn', 'Uranus', 'Neptune']`. Use the form you read most easily.

### A variation to try

Print the two planets with the longest years, with their periods, from the longest:

```python
top = planets.sort_values("Orbital period (days)", ascending=False).head(2)
print(top[["Planet", "Orbital period (days)"]].to_string(index=False))
```

```text
 Planet  Orbital period (days)
Neptune                59800.0
 Uranus                30589.0
```

### If your output differs

1. **`KeyError`**: print `planets.columns` and copy the exact name.
2. **An empty list**: you took another table; print `len(tables)` and `tables[0].head()`.
3. **`ValueError: No tables found`**: the address is wrong, or the page did not load; print `html[:200]`.

---

## Exercise 7.2 (medium)

> Read only the league table with `match="Points"`, flatten its header, remove the footnote mark, and print the team and the points of teams with more than 30 points. Expected output:

**What the question asks.** Read one specific table, the league, among several; turn its two-row header into simple names; clean the footnote marks out of the team names; then filter on points.

**The plan.** `read_html(..., match="Points")` keeps only tables containing the word *Points*. Build new column names from the pairs pandas gives. Remove `[a]`-style marks with a regular expression. Filter and select with `.loc`.

```python
from io import StringIO

import pandas as pd
import requests

html = requests.get("http://localhost:8000/tables/", timeout=10).text
league = pd.read_html(StringIO(html), match="Points")[0]
league.columns = [
    b if a == b else f"{a} {b}" for a, b in league.columns
]
league["Team"] = league["Team"].str.replace(
    r"\s*\[[^\]]*\]", "", regex=True
)
print(league.loc[league["Points"] > 30, ["Team", "Points"]].to_string())
```

Output:

```text
                   Team  Points
0      Riverside Rovers      45
1          Harbour Town      40
2        Kestrel United      36
3  Copperfield Athletic      32
```

**Line by line.**

- `match="Points"` keeps only the tables whose text contains *Points*: here, one table.
- The league's header has two rows (`Results` above `Won`, `Drawn`, `Lost`), so pandas gives each column a pair, such as `("Results", "Won")`, or `("Team", "Team")` where one cell spans both rows.
- `[b if a == b else f"{a} {b}" for a, b in league.columns]` builds one name per pair: `Team` when both parts are the same, `Results Won` otherwise.
- `.str.replace(r"\s*\[[^\]]*\]", "", regex=True)` removes any space followed by `[`, anything that is not `]`, and `]`: `Harbour Town[a]` becomes `Harbour Town`.
- `league.loc[league["Points"] > 30, ["Team", "Points"]]` keeps the rows with more than 30 points and the two columns.

**Reading the result.** Four teams above 30 points, led by Riverside Rovers with 45. The row numbers on the left are the table's own positions, 0 to 3.

**Checking.** `print(league.columns.tolist())` shows `['Pos', 'Team', 'Results Won', 'Results Drawn', 'Results Lost', 'Points']`. `print(league["Team"].tolist())` shows no `[a]` left.

**Mistakes this exercise provokes.**

- Skipping the header step: `league["Points"]` still works (pandas finds the pair), but `league["Results Won"]` fails, and printed tables show two header rows.
- `str.replace("[a]", "")` removes that one mark but not `[b]` or `[1]`; the regular expression removes any of them.
- `match="Team"` could match several tables on another page; `[0]` then silently takes the first. Check with `len()`.

**The choice it makes.** `match` relies on a word only one table contains. Check such guesses with `len()`: if `match` keeps more than one table, `[0]` silently takes the first one.

### Another way to solve it

`header=1` tells pandas to use only the second header row, which gives simple names at once:

```python
league = pd.read_html(StringIO(html), match="Points", header=1)[0]
print(league.columns.tolist())
```

```text
['Pos', 'Team', 'Won', 'Drawn', 'Lost', 'Points']
```

Shorter, but the word *Results* is lost. The book's version keeps it in the names, which matters when two groups of columns share sub-headings.

### A variation to try

Add a column of points per game (a win is 3 points): `league["Played"] = league["Results Won"] + league["Results Drawn"] + league["Results Lost"]`, then `league["Points"] / league["Played"]`. Sort by it: is the order the same as by points?

### If your output differs

1. **`[a]` still in a name**: the `regex=True` argument is missing, so the pattern was read as plain text.
2. **`KeyError: 'Team'`** after renaming: print `league.columns` before and after the renaming line.
3. **`IndexError: list index out of range`**: `match` found no table; check the word and the address.

---

## Exercise 7.3 (medium)

> Read `http://localhost:8000/files/` with `read_html`, and print the total size of all the files, in bytes. Expected output:

**What the question asks.** One number: the total size of the files listed on the Files page, computed by pandas instead of a loop.

**The plan.** Read the table `#file-list` with `read_html`, then add up its size column with `.sum()`.

```python
from io import StringIO

import pandas as pd
import requests

html = requests.get("http://localhost:8000/files/", timeout=10).text
files = pd.read_html(StringIO(html), attrs={"id": "file-list"})[0]
print(files["Size (bytes)"].sum(), "bytes")
```

Output:

```text
21804 bytes
```

**Line by line.**

- `attrs={"id": "file-list"}` tells `read_html` to keep only the table whose `id` is `file-list`.
- `[0]` takes that table from the list `read_html` returns.
- `files["Size (bytes)"]` is the size column; pandas already read it as numbers.
- `.sum()` adds up the column.

**Reading the result.** 21,804 bytes for six files, about 21 kilobytes in all.

**Checking.** Compare with exercise 6.2: the six sizes printed there add up to the same total. `print(files.dtypes)` shows `int64` for the size column.

**Mistakes this exercise provokes.**

- `files["Size"]`: `KeyError`; the column is called `Size (bytes)`, as on the page.
- Forgetting `[0]`: `read_html` returns a list, and a list has no columns.
- Summing a column read as text: pandas would glue the texts together instead of adding numbers. Check `.dtypes`.

**The choice it makes.** Compare with exercise 6.2: the same table, without a loop. When the data is a real HTML table, `read_html` is always shorter, and it converts the numbers for you.

### Another way to solve it

Without `attrs`: the Files page holds a single table, so `pd.read_html(StringIO(html))[0]` gives the same DataFrame. `attrs` protects you on the day the page gains a second table.

### A variation to try

Answer three more questions with the same DataFrame:

```python
print(files["Size (bytes)"].mean().round())                 # 3634.0
print(files.loc[files["Size (bytes)"].idxmax(), "File"])    # market_report_q4_2026.xlsx
print(files[files["File"].str.endswith(".xlsx")]["Size (bytes)"].sum())  # 11919
```

`idxmax()` gives the row label of the largest value; `.str.endswith(".xlsx")` keeps the Excel files.

### If your output differs

1. **`KeyError`**: print `files.columns`.
2. **A total made of digits glued together**: the column is text; check `files.dtypes`.

---

## Exercise 7.4 (harder)

> Print the average rate of each bank from the savings table, ignoring the missing rate, sorted from the highest. Use `rates.groupby("Bank")["Rate"].mean()`. Expected output:

**What the question asks.** An average per group: for each bank of the savings table, the mean of its account rates, ignoring the account whose rate is missing, from the highest average to the lowest.

**The plan.** Read the savings table, turn the rate texts (`3.10%`) into numbers, then `groupby("Bank")` and `mean()`, and sort.

```python
from io import StringIO

import pandas as pd
import requests

html = requests.get("http://localhost:8000/tables/", timeout=10).text
rates = pd.read_html(StringIO(html), match="Minimum deposit",
                     na_values=["n/a"])[0]
rates["Rate"] = rates["Rate"].str.rstrip("%").astype(float)
average = rates.groupby("Bank")["Rate"].mean().sort_values(ascending=False)
print(average.round(2))
```

Output:

```text
Bank
Harbour Building Society    5.50
Northbridge Bank            3.58
Kestrel Direct              3.45
Name: Rate, dtype: float64
```

**Line by line.**

- `match="Minimum deposit"` keeps the savings table, the only one containing those words.
- `na_values=["n/a"]` reads `n/a` as a missing value, `NaN`.
- `rates["Rate"].str.rstrip("%")` removes the `%` at the end of each text; `.astype(float)` turns the result into numbers. `NaN` stays `NaN`.
- `rates.groupby("Bank")` gathers the rows of each bank; `["Rate"].mean()` computes the average rate of each group.
- `.sort_values(ascending=False)` puts the highest first; `.round(2)` keeps two decimals.

**Reading the result.** Harbour Building Society first with 5.50%, its single account. Northbridge Bank averages 3.58% from two accounts (3.10% and 4.05%). Kestrel Direct shows 3.45%, the rate of its only known account: `mean()` ignores `NaN`.

**Checking.** Work out Northbridge by hand: (3.10 + 4.05) / 2 = 3.575. Print `rates` to see all five accounts and the missing rate.

**Mistakes this exercise provokes.**

- `.astype(float)` without `rstrip("%")`: `ValueError: could not convert string to float: '3.10%'`.
- `rates.groupby("Bank").mean()` without choosing the column: pandas tries to average every column, including text ones, and stops with `TypeError: dtype 'str' does not support operation 'mean'`.
- Replacing the missing rate with 0 (`fillna(0)`): Kestrel Direct's average falls to 1.72%, a number that describes no account.

**The choice it makes.** Ignoring the missing rate is right for an average. For a count of accounts, you would keep it: `rates.groupby("Bank").size()` counts every row, `rates.groupby("Bank")["Rate"].count()` counts only the known rates. Decide which question you are answering.

### Another way to solve it

`agg` computes several statistics per group at once, which shows the missing rate clearly:

```python
print(rates.groupby("Bank")["Rate"].agg(["mean", "count", "size", "max"]))
```

```text
                           mean  count  size   max
Bank                                              
Harbour Building Society  5.500      1     1  5.50
Kestrel Direct            3.450      1     2  3.45
Northbridge Bank          3.575      2     2  4.05
```

Kestrel Direct has `size` 2 (two accounts) but `count` 1 (one known rate): that gap is the missing value.

### A variation to try

Remove `na_values=["n/a"]` and run again: the result is the same, because pandas already treats `n/a` as missing by default. Writing it anyway documents what the page uses for a gap, and protects you when a page uses a word pandas does not know, such as `none` or `–`.

### If your output differs

1. **`ValueError: could not convert string to float: '3.10%'`**: the `rstrip("%")` step is missing.
2. **Kestrel Direct at 1.72**: the missing rate was replaced by 0; remove the `fillna`.
3. **`3.575` instead of `3.58`**: add `.round(2)`.
