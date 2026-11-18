# Chapter 13 — detailed solutions

These are the solutions printed in the book, word for word: what the question asks, the plan, the code, line by line, reading the result, checking, the mistakes the exercise provokes, the choice it makes, another way to solve it, a variation to try, and what to do if your output differs. Here, each program is followed by its exact output.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 13.1 (easy)

> Use `re.findall` to print every number of the text `"Rooms: 3, floor 12, built 1998, price £245,000"`, then the price alone as an integer. Expected output:

**What the question asks.** Two separate results from the same sentence. First, *every* number, as a list: this shows you what a simple pattern does with a real sentence. Second, *one* number, the price, as a Python `int`: a value you can add, compare and store, not the text `"245,000"`.

**The plan.**

1. Find every run of digits with `re.findall(r"\d+", text)`.
2. Find the price by anchoring on what comes before it, the `£` sign, and accept the commas inside it: `£([\d,]+)`.
3. Keep only the part in brackets, remove the commas, convert to `int`.

```python
import re

text = "Rooms: 3, floor 12, built 1998, price £245,000"
print(re.findall(r"\d+", text))
price = re.search(r"£([\d,]+)", text).group(1)
print(int(price.replace(",", "")))
```

Output:

```text
['3', '12', '1998', '245', '000']
245000
```

**Line by line.**

- `import re` loads Python's regular-expression module. It is part of Python; there is nothing to install.
- `text = ...` is the sentence. On a real page this text would come from `.text` on an element.
- `re.findall(r"\d+", text)`:
  - `\d` means *one digit* (0 to 9); `+` means *one or more of what comes before*. Together: *a run of digits*.
  - `findall` scans the whole text from left to right and returns **every** match, as a list of strings.
  - The `r` before the quotes makes a *raw string*: Python leaves `\d` as written instead of trying to interpret the backslash.
- `re.search(r"£([\d,]+)", text)`:
  - `search` returns the **first** match only, as a *match object*, or `None` if there is none.
  - `£` must be there literally, so the match starts at the price and nowhere else.
  - `[\d,]` is a *character class*: one character that is either a digit or a comma. With `+`: a run of digits and commas.
  - The brackets `( )` form a *group*. `.group(1)` returns what the first group matched, `"245,000"`; `.group(0)` would return the whole match, `"£245,000"`.
- `price.replace(",", "")` gives `"245000"`. `int(...)` converts it to the number 245000, and `print` shows it without quotes.

**Reading the result.** The first line has **five** items for four numbers. `245,000` became `'245'` and `'000'`, because a comma is not a digit: `\d+` stops at the comma and starts a new match after it. This is the most common surprise with numbers in scraped text, which is why the price needs its own pattern.

The second line is `245000`, with no quotes: it is an `int`, not a string.

**Checking.**

- `print(type(int(price.replace(",", ""))))` prints `<class 'int'>`.
- `print(int(price.replace(",", "")) + 1)` prints `245001`: you can calculate with it.
- Count the numbers in the sentence yourself: 3, 12, 1998, 245,000. The list has one item more, for the reason above.

**Mistakes this exercise provokes.**

| What you wrote | What happens | Fix |
|---|---|---|
| `re.search(r"£(\d+)", text)` | `245`: the comma stops `\d+` | accept commas: `[\d,]+` |
| `int("245,000")` | `ValueError: invalid literal for int() with base 10: '245,000'` | `.replace(",", "")` first |
| `re.search(...)` without `.group(1)` | prints `<re.Match object; span=(38, 46), match='£245,000'>` | add `.group(1)` |
| `"\d+"` without `r` | works, but Python 3.12+ prints `SyntaxWarning: invalid escape sequence '\d'` | always `r"..."` for patterns |
| `re.findall(r"£([\d,]+)", text)[0]` | works too, but builds a list for one value | `search` when you want one |

**The choice it makes.** `[\d,]+` is permissive: it would also accept `1,,2` or `,,,`. Section 13.2 of the book uses a strict pattern, `\d+(?:,\d{3})*`, which accepts commas only between groups of three digits. On a page whose format you know, the short pattern is easier to read and enough; on text you do not control, use the strict one.

**Another way to solve it.** The strict pattern of section 13.2 keeps `245,000` whole in the list itself:

```python
print(re.findall(r"\d+(?:,\d{3})*", text))
```

```text
['3', '12', '1998', '245,000']
```

`(?:,\d{3})*` means *zero or more groups of a comma followed by exactly three digits*. `(?: )` groups without capturing, so `findall` still returns the whole match. Note that `3, 12` stays two numbers: the comma there is followed by a space, not three digits.

**A variation to try.** Extract both prices from `"Was £1,299.50, now £1,099.00"` as floats. You need commas **and** decimals:

```python
t2 = "Was £1,299.50, now £1,099.00"
print(re.findall(r"£(\d+(?:,\d{3})*(?:\.\d+)?)", t2))
```

```text
['1,299.50', '1,099.00']
```

Then convert each with `float(x.replace(",", ""))`. Which is the current price? The last one: `re.findall(...)[-1]`.

**If your output differs.**

1. **`AttributeError: 'NoneType' object has no attribute 'group'`**: `search` found nothing. Print `repr(text)`: your text may use a different character, such as `GBP` or a non-breaking space after `£`.
2. **Only four items in the first list**: you used the strict pattern, which is correct but not what the exercise asked; compare with the output above.
3. **`245000` printed with quotes**: you printed the string, not the `int`.

---

## Exercise 13.2 (medium)

> Scrape the job board (page 1 only), build a DataFrame with `title`, `city`, `salary` (the text) and `posted` (from the `datetime` attribute), then add the columns `salary_min`, `salary_max` (integers, with a regular expression) and `age_days` (days between `posted` and 2027-03-01). Print the three newest jobs. Expected output:

**What the question asks.** A table you can calculate with. The page shows salaries as text (`£75,000 – £89,000`) and dates as attributes; the exercise asks you to turn both into numbers, then use them to sort.

**The plan.**

1. Download page 1 and parse it, as in Chapter 11.
2. Build one dictionary per job, then a DataFrame.
3. Add `salary_min` and `salary_max` with a regular expression applied to every row.
4. Convert `posted` to dates and subtract from 1 March 2027.
5. Sort by age, keep three rows, print.

```python
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

soup = BeautifulSoup(
    requests.get("http://localhost:8000/jobs/", timeout=10).text,
    "html.parser",
)
rows = [
    {
        "title": li.select_one("h2 a").text,
        "city": li.select_one("p.location").text,
        "salary": li.select_one("p.salary").text,
        "posted": li.select_one("p.posted time")["datetime"],
    }
    for li in soup.select("li.job")
]
jobs = pd.DataFrame(rows)

amounts = jobs["salary"].apply(
    lambda s: [
        int(x.replace(",", "")) for x in re.findall(r"[\d,]+", s)
    ]
)
jobs["salary_min"] = amounts.str[0]
jobs["salary_max"] = amounts.str[1]
jobs["posted"] = pd.to_datetime(jobs["posted"])
jobs["age_days"] = (pd.Timestamp("2027-03-01") - jobs["posted"]).dt.days
print(
    jobs.sort_values("age_days")[
        ["title", "city", "salary_min", "age_days"]
    ]
    .head(3)
    .to_string(index=False)
)
```

Output:

```text
                     title       city  salary_min  age_days
Senior Credit Risk Analyst      Leeds       75000         0
       Junior Data Analyst Manchester       37000         0
          Senior QA Tester       Lyon       67000         0
```

**Line by line.**

- `requests.get(..., timeout=10).text` downloads the page; `BeautifulSoup(..., "html.parser")` turns it into a tree.
- The list comprehension `[{...} for li in soup.select("li.job")]` builds one dictionary per job card:
  - `li.select_one("h2 a").text` is the title, the text of the link inside `h2`;
  - `p.location` and `p.salary` are the city and the salary text;
  - `li.select_one("p.posted time")["datetime"]` reads the **attribute** of the `<time>` tag, such as `2027-03-01`, not its visible text. Attributes in ISO format are made for programs; the visible text is made for people and may change (*today*, *2 days ago*).
- `pd.DataFrame(rows)` turns the list of dictionaries into a table: one row per dictionary, one column per key.
- The salary step, from the inside out:
  - `re.findall(r"[\d,]+", s)` on `£75,000 – £89,000` returns `["75,000", "89,000"]`;
  - `int(x.replace(",", ""))` converts each to an integer;
  - `lambda s: [...]` packages that as a small function of one salary text;
  - `.apply(...)` calls it on every row, so `amounts` is a column whose values are lists: `[75000, 89000]`.
- `amounts.str[0]` takes item 0 of each list, `amounts.str[1]` item 1. The `.str` accessor works on lists as well as on text.
- `pd.to_datetime(jobs["posted"])` converts the column from text to dates.
- `pd.Timestamp("2027-03-01") - jobs["posted"]` subtracts every date from 1 March 2027 and gives *durations*; `.dt.days` turns each duration into a whole number of days.
- `jobs.sort_values("age_days")` sorts from the newest (age 0) to the oldest; `[[...]]` keeps four columns; `.head(3)` keeps three rows; `.to_string(index=False)` prints without the row numbers on the left.

**Reading the result.** Three jobs posted on 1 March 2027 itself (`age_days` 0). The salaries are plain integers: `75000`, not `£75,000`. That is what lets you sort, average or filter them.

**Checking.**

- `print(jobs.dtypes)` shows `int64` for `salary_min`, `salary_max` and `age_days`, and a `datetime64` type for `posted`.
- `print((jobs["salary_min"] <= jobs["salary_max"]).all())` prints `True`: no range is upside down.
- `print(len(jobs))` prints `15`: page 1 holds 15 offers.
- Open the job board in the browser and compare the first row with the page.

**Mistakes this exercise provokes.**

| What you wrote | What happens | Fix |
|---|---|---|
| `li.select_one("p.posted").text` | the visible text, harder to convert | read the `datetime` attribute |
| subtracting before `pd.to_datetime` | `TypeError`: you cannot subtract text from a date | convert first |
| `re.findall(r"\d+", s)` | `["75", "000", "89", "000"]` | accept commas: `[\d,]+` |
| `amounts[0]` instead of `amounts.str[0]` | the first **row**, `[75000, 89000]` | `.str[0]` for the first **item of each row** |
| `.head(3)` without sorting | the first three on the page, whatever their age | `sort_values` first |

Several jobs share age 0, so which three appear depends on the order of the page. When the order must be the same every time, sort on two columns: `sort_values(["age_days", "title"])`.

**The choice it makes.** One regular expression returns both salaries in one pass. Splitting the text on `–` also works today, but breaks the day the site writes `to` or a plain hyphen. Matching the numbers themselves is more robust than matching the separator between them.

**Another way to solve it.** pandas can apply a regular expression with groups to a whole column at once, without `apply` and `lambda`:

```python
parts = jobs["salary"].str.extract(r"£([\d,]+)\D+£([\d,]+)")
print(parts.head(2))
```

```text
        0       1
0  75,000  89,000
1  37,000  50,000
```

`.str.extract` returns one column per group. `\D+` means *one or more characters that are not digits*: the space, the dash and the space between the two amounts. Then convert each column: `parts[0].str.replace(",", "").astype(int)`. This version is faster on large tables; the book's version is easier to follow step by step.

**A variation to try.** Which city pays the highest minimum salary on average? Add three lines after `salary_min`:

```python
print(
    jobs.groupby("city")["salary_min"].mean().round()
    .sort_values(ascending=False).head(3).to_string()
)
```

```text
city
Paris    62000.0
Lyon     58400.0
Leeds    57400.0
```

**If your output differs.**

1. **`TypeError: 'NoneType' object is not subscriptable`**: a selector found nothing. Print `soup.select_one("li.job")` to see the real structure of one card.
2. **A different `age_days`**: you started the site with `--live` or `--date`; restart it with `python run_site.py`, which fixes the date to 1 March 2027.
3. **Different titles with age 0**: see the tie note above; the order of equal ages follows the page.

---

## Exercise 13.3 (medium)

> Read `bank_capital_eu.csv` correctly and print, for each country, the lowest CET1 ratio under the adverse scenario, all years. Expected output:

**What the question asks.** The file uses European conventions: semicolons between columns, a comma as the decimal mark (`14,63`) and dots between thousands (`850.263,5`). "Correctly" means that every number column is read as a number. Then a filter and a group.

**The plan.**

1. Look at the first lines of the file before writing code (in the browser, or with `print(requests.get(url).text[:300])`).
2. Tell `read_csv` the three conventions.
3. Keep the adverse rows; group by country; take the minimum; sort.

```python
import pandas as pd

banks = pd.read_csv(
    "http://localhost:8000/files/bank_capital_eu.csv",
    sep=";",
    decimal=",",
    thousands=".",
)
adverse = banks[banks["Scenario"] == "Adverse"]
print(
    adverse.groupby("Country")["CET1 ratio (%)"]
    .min()
    .sort_values()
    .to_string()
)
```

Output:

```text
Country
DE    10.09
IT    10.11
ES    10.53
FR    11.62
NL    12.46
UK    12.64
```

**Line by line.**

- `pd.read_csv(url, ...)` reads straight from the address; pandas downloads the file itself.
- `sep=";"`: the column separator. The default is a comma.
- `decimal=","`: the character that separates the decimals, so `14,63` is read as 14.63.
- `thousands="."`: the character between groups of thousands, ignored when reading, so `850.263,5` becomes 850263.5.
- `banks["Scenario"] == "Adverse"` produces a column of `True`/`False`; `banks[...]` keeps the rows where it is `True`.
- `.groupby("Country")["CET1 ratio (%)"]` splits the ratios by country; `.min()` keeps the lowest of each group.
- `.sort_values()` sorts from lowest to highest; `.to_string()` prints every row.

**Reading the result.** Six countries, one line each. Germany has the lowest ratio under stress, 10.09%; the United Kingdom the highest of the six, 12.64%. A CET1 ratio is a bank's core capital as a percentage of its risk-weighted assets: the lower, the less buffer against losses.

**Checking.**

- `print(banks.dtypes)` shows `float64` for `Total assets (EUR m)` and `CET1 ratio (%)`.
- `print(len(banks))` prints `24`: six countries × two years (2024, 2025) × two scenarios.
- `print(len(adverse))` prints `12`.
- `print(adverse[adverse["Country"] == "DE"])` shows the two German rows; the smaller ratio is the one printed.

**Mistakes this exercise provokes.** What happens when you leave the options out, run on the real file:

```python
raw = pd.read_csv(url)
print(raw.shape)
```

```text
(24, 1)
```

One column: without `sep=";"`, every line is a single piece of text. With `sep=";"` but without the other two options, both number columns come back as text (`str` in pandas 3), and `.min()` then compares text, character by character.

| What you wrote | What happens | Fix |
|---|---|---|
| no `sep` | one column | `sep=";"` |
| no `decimal` | ratios are text: `"14,63"` | `decimal=","` |
| no `thousands` | total assets are text | `thousands="."` |
| `"adverse"` in lower case | empty result, no error | copy the value from the file |

**The choice it makes.** Giving `read_csv` the conventions reads the file correctly once, for every column. Cleaning afterwards with `.str.replace(",", ".")` works too, but must be repeated for each column and is easy to forget for one.

**Another way to solve it.** Compare the two scenarios bank by bank: how much does the stress lower the ratio? `pivot_table` puts the scenarios side by side:

```python
wide = banks.pivot_table(
    index=["Country", "Year"], columns="Scenario", values="CET1 ratio (%)"
)
wide["drop"] = (wide["Baseline"] - wide["Adverse"]).round(2)
print(wide.sort_values("drop", ascending=False).head(3).to_string())
```

```text
Scenario      Adverse  Baseline  drop
Country Year                         
DE      2024    10.09     16.87  6.78
IT      2024    10.93     16.46  5.53
NL      2024    12.46     17.24  4.78
```

**A variation to try.** Print the lowest adverse ratio **per year** rather than over both years: group by two columns, `adverse.groupby(["Country", "Year"])["CET1 ratio (%)"].min()`. You get 12 lines.

**If your output differs.**

1. **`KeyError: 'Scenario'`**: the separator is wrong, so the column names are wrong; print `banks.columns`.
2. **Ratios such as `1463.0`**: you swapped `decimal` and `thousands`.
3. **An empty result**: check the exact spelling of `"Adverse"` with `print(banks["Scenario"].unique())`.

---

## Exercise 13.4 (medium)

> Scrape pages 1 and 2 of the library twice each (four requests), build a DataFrame, and show that it has 80 rows but only 40 distinct books. Save the clean 40 to `output/ch13/books_p1_p2.csv`. Expected output:

**What the question asks.** To reproduce on purpose the most common accident of a scraper, reading the same pages twice (after a restart, or because two links lead to the same page), then to prove the duplicates exist with numbers, and to remove them.

**The plan.**

1. Loop over the pages 1, 2, 1, 2.
2. Collect one dictionary per book card, with the book's identifier.
3. Build the DataFrame; count rows; drop duplicates on the identifier; count again.
4. Save the clean table.

```python
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

session = requests.Session()
rows = []
for page in [1, 2, 1, 2]:
    url = f"http://localhost:8000/library/page-{page}.html"
    soup = BeautifulSoup(
        session.get(url, timeout=10).text, "html.parser"
    )
    for card in soup.select("article.book-card"):
        rows.append(
            {
                "id": int(card["data-id"]),
                "title": card.select_one("h3 a")["title"],
                "rating": card.select_one("p.star-rating")["class"][1],
                "price": float(card.select_one("p.price").text[1:]),
            }
        )
books = pd.DataFrame(rows)
clean = books.drop_duplicates(subset="id")
print(len(books), "rows,", len(clean), "distinct books")
Path("output/ch13").mkdir(parents=True, exist_ok=True)
clean.to_csv("output/ch13/books_p1_p2.csv", index=False)
```

Output:

```text
80 rows, 40 distinct books
```

**Line by line.**

- `requests.Session()` keeps one connection open for the four requests, which is faster and politer than four separate connections.
- `for page in [1, 2, 1, 2]` is the duplication, written explicitly.
- `f"http://localhost:8000/library/page-{page}.html"` builds the address of each page.
- For each `article.book-card`:
  - `int(card["data-id"])` reads the identifier the site gives each book, an attribute you do not see on the page;
  - `card.select_one("h3 a")["title"]` reads the full title from the link's `title` attribute (the visible text may be cut short);
  - `["class"][1]` takes the second class of the rating paragraph: for `class="star-rating Three"`, BeautifulSoup returns `["star-rating", "Three"]`;
  - `.text[1:]` drops the first character, `£`, and `float(...)` converts the rest.
- `books.drop_duplicates(subset="id")` keeps the **first** row of each identifier and drops the others.
- `Path("output/ch13").mkdir(parents=True, exist_ok=True)` creates the folders if needed, and does nothing if they exist.
- `clean.to_csv(..., index=False)` writes the file without the row numbers.

**Reading the result.** `80 rows, 40 distinct books`: four pages of 20 cards, and each of the 40 books twice. Exercise 13.5 reads the file this program saves.

**Checking.**

- `print(books.duplicated(subset="id").sum())` prints `40`: the number of rows that repeat an earlier identifier.
- `print(books.groupby("id").size().value_counts())` shows that all 40 identifiers appear exactly twice.
- `print(clean["id"].is_unique)` prints `True`.
- Open `output/ch13/books_p1_p2.csv`: 41 lines, the header and 40 books.

**Mistakes this exercise provokes.**

| What you wrote | What happens | Fix |
|---|---|---|
| `drop_duplicates()` | works here; on a live site, a price that changed between two reads keeps both rows | `subset="id"` |
| `subset="title"` | two different books with the same title lose one | deduplicate on an identifier |
| `to_csv(...)` without `index=False` | an extra unnamed column of 0, 1, 2… | `index=False` |
| forgetting `mkdir` | `OSError: Cannot save file into a non-existent directory` | create the folder first |

**The choice it makes.** `subset="id"` trusts the site's identifier. It is the safest key when it exists. `keep="first"` (the default) keeps the oldest copy; `keep="last"` keeps the newest, which matters when the two reads differ, for example a price that changed between them.

**Another way to solve it.** When a site gives no identifier, use the address of the detail page, which is unique for each item. Add `"url": card.select_one("h3 a")["href"]` to the dictionary and write `books.drop_duplicates(subset="url")`: it also gives 40 rows.

**A variation to try.** Do not create the duplicates at all: keep a set of the identifiers you have seen and skip a card whose identifier is already in it.

```python
seen = set()
...
        book_id = int(card["data-id"])
        if book_id in seen:
            continue
        seen.add(book_id)
```

The DataFrame then has 40 rows from the start. This is the method of Chapter 23's crawler.

**If your output differs.**

1. **`40 rows, 40 distinct books`**: your loop reads each page once; check the list `[1, 2, 1, 2]`.
2. **`80 rows, 80 distinct books`**: you deduplicated on a column that differs between reads, or forgot `subset`.
3. **`KeyError: 'data-id'`**: you selected another element than `article.book-card`.

---

## Exercise 13.5 (harder)

> Save the clean books of exercise 13.4 to an SQLite table `books`, then use one SQL query to print the number of books and the average price per rating, highest rating first. Expected output:

**What the question asks.** To move the data into a database and let the database answer a question: for each rating, how many books, and their average price. One query, not a loop.

**The plan.**

1. Read the CSV saved by exercise 13.4.
2. Turn the rating words (`Three`) into numbers (3), so that they sort correctly.
3. Write the table with `to_sql`.
4. Write a `GROUP BY` query and run it with `pd.read_sql`.

```python
import sqlite3

import pandas as pd

books = pd.read_csv("output/ch13/books_p1_p2.csv")
words = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
books["rating"] = books["rating"].map(words)
with sqlite3.connect("output/ch13/books.db") as db:
    books.to_sql("books", db, if_exists="replace", index=False)
    query = """
        SELECT rating, COUNT(*) AS books, ROUND(AVG(price), 2) AS avg_price
        FROM books GROUP BY rating ORDER BY rating DESC
    """
    print(pd.read_sql(query, db).to_string(index=False))
```

Output:

```text
 rating  books  avg_price
      5      9      31.95
      4      4      36.72
      3     14      27.35
      2      6      39.20
      1      7      31.08
```

**Line by line.**

- `pd.read_csv("output/ch13/books_p1_p2.csv")` reads the 40 books. Run exercise 13.4 first.
- `words = {"One": 1, ...}` is the translation table.
- `books["rating"].map(words)` replaces each value by `words[value]`. A value missing from the dictionary would become `NaN`.
- `with sqlite3.connect("output/ch13/books.db") as db:` opens the database file, creating it if needed. At the end of the block, what was written is committed.
- `books.to_sql("books", db, if_exists="replace", index=False)` creates the table `books`, with one column per DataFrame column, and inserts the 40 rows. `replace` drops an existing table first, so you can run the program again.
- The query, clause by clause:
  - `SELECT rating, COUNT(*) AS books, ROUND(AVG(price), 2) AS avg_price`: the three columns of the answer; `AS` names them.
  - `FROM books`: the table.
  - `GROUP BY rating`: one group per rating value; `COUNT(*)` and `AVG(price)` are computed inside each group.
  - `ORDER BY rating DESC`: highest rating first.
- `pd.read_sql(query, db)` sends the query and returns the answer as a DataFrame.

**Reading the result.** Five rows. Three-star books are the most frequent (14 of 40). Two-star books are the most expensive on average (£39.20) and three-star books the cheapest (£27.35): on these 40 books, a better rating does not mean a higher price.

**Checking.**

- The `books` column adds up to 40: 9 + 4 + 14 + 6 + 7.
- The same answer in pandas:

```python
print(
    books.groupby("rating")
    .agg(books=("price", "size"), avg_price=("price", "mean"))
    .round(2).sort_index(ascending=False).to_string()
)
```

```text
        books  avg_price
rating                  
5           9      31.95
4           4      36.72
3          14      27.35
2           6      39.20
1           7      31.08
```

**Mistakes this exercise provokes.**

| What you wrote | What happens | Fix |
|---|---|---|
| keeping the words | `ORDER BY rating DESC` sorts the words: Two, Three, One, Four, Five | `.map(words)` first |
| `if_exists="append"` | each run adds 40 rows; the counts double, then triple | `replace` for a table you rebuild |
| running 13.5 first | `FileNotFoundError: ... books_p1_p2.csv` | run 13.4 first |
| `AVG(price)` without `ROUND` | `31.950000000000003`: floating-point noise | `ROUND(..., 2)` |
| `SELECT rating, title, COUNT(*)` | SQLite returns one title per group, chosen without rule | select only grouped or aggregated columns |

**The choice it makes.** For 40 rows, pandas and SQL give the same answer and pandas needs no database. SQL is worth it when the data already lives in a database, when it is too large to load into memory, or when several programs share it, as in Chapters 22 and 24.

**Another way to solve it.** `HAVING` filters groups after they are counted, where `WHERE` filters rows before. Only the ratings with at least 7 books, most frequent first:

```sql
SELECT rating, COUNT(*) AS books
FROM books
GROUP BY rating
HAVING COUNT(*) >= 7
ORDER BY books DESC
```

```text
 rating  books
      3     14
      5      9
      1      7
```

**A variation to try.** Add the cheapest and most expensive price of each rating: `MIN(price)` and `MAX(price)` in the `SELECT`. Then answer: is the most expensive of the 40 books well rated?

**If your output differs.**

1. **Counts of 18, 8, 28…**: the table holds two copies; you used `append`, or exercise 13.4's file kept duplicates.
2. **`NaN` in `rating`**: a word is missing from `words` or spelt differently; print `books["rating"].unique()` before the `map`.
3. **`sqlite3.OperationalError: no such table: books`**: `to_sql` did not run on the same connection, or ran with another table name.
