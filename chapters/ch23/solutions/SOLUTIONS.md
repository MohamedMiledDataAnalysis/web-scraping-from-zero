# Chapter 23 — detailed solutions

These are the solutions printed in the book, word for word: what the question asks, the plan, the code, line by line, reading the result, checking, the mistakes the exercise provokes, the choice it makes, another way to solve it, a variation to try, and what to do if your output differs. Here, each program is followed by its exact output.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 23.1 (easy)

> From `catalogue.xlsx`, print the three categories with the highest average price. Expected output:

**What the question asks.** Read the project's Excel file and print the three categories whose books cost most on average.

**The plan.** The workbook already has a *Summary* sheet with one row per category and its average price; read that sheet and keep the three largest values.

```python
import pandas as pd

summary = pd.read_excel(
    "output/ch23/catalogue.xlsx", sheet_name="Summary"
)
print(
    summary.nlargest(3, "avg_price")[
        ["category", "avg_price"]
    ].to_string(index=False)
)
```

Output:

```text
 category  avg_price
  Fiction      39.71
  History      36.72
Self Help      36.50
```

**Line by line.**

- `pd.read_excel("output/ch23/catalogue.xlsx", sheet_name="Summary")` reads one sheet of the workbook into a DataFrame: 20 rows, one per category.
- `summary.nlargest(3, "avg_price")` returns the three rows with the largest `avg_price`, largest first.
- `[["category", "avg_price"]]` keeps the two columns to show.
- `to_string(index=False)` prints without the row numbers.

**Reading the result.** Fiction is the most expensive category on average (£39.71), then History (£36.72) and Self Help (£36.50).

**Checking.** Recompute from the *Catalogue* sheet: `books.groupby("category")["price"].mean().nlargest(3).round(2)` gives the same three categories and averages. The next one, Business at £36.19, is close behind Self Help.

**Mistakes this exercise provokes.**

- `pd.read_excel("output/ch23/catalogue.xlsx")` without `sheet_name`: pandas reads the **first** sheet, *Catalogue*, which has no `avg_price` column (`KeyError`).
- `sort_values("avg_price").head(3)`: the three **cheapest** categories, because sorting is ascending by default.
- Running before `final.py`: the workbook does not exist yet (`FileNotFoundError`).

**The choice it makes.** Reading the summary trusts the numbers the project computed; recomputing from the catalogue checks them. In a report, read the summary; when a number looks surprising, recompute it from the rows.

**Another way to solve it.** Recompute from the rows, as in the check:

```python
books = pd.read_excel("output/ch23/catalogue.xlsx", sheet_name="Catalogue")
print(books.groupby("category")["price"].mean().nlargest(3).round(2))
```

The same three categories. This version does not depend on how the summary was built, so it keeps working if someone edits the *Summary* sheet by hand.

**A variation to try.** Averages hide spread. Add the cheapest and the most expensive book of each category: `books.groupby("category")["price"].agg(["mean", "min", "max"])`. Then look at the number of books per category (`books` column of the summary): an average over 47 books is more stable than one over 10.

**If your output differs.**

1. **`KeyError: 'avg_price'`**: you read the *Catalogue* sheet; pass `sheet_name="Summary"`.
2. **`ImportError: Missing optional dependency 'openpyxl'`**: install the requirements of the repository.

---

## Exercise 23.2 (medium)

> Is there a link between rating and price? Print the average price per rating, and the correlation between the two columns (`books["price"].corr(books["rating"])`), rounded to three decimals. Expected output:

**What the question asks.** Test a common belief: do better-rated books cost more? Compare the average price of each rating level, then measure the link with one number, the correlation.

**The plan.** Group the 1,000 books by rating and average their prices; then compute the correlation between the two columns.

```python
import pandas as pd

books = pd.read_excel("output/ch23/catalogue.xlsx", sheet_name="Catalogue")
print(books.groupby("rating")["price"].mean().round(2).to_string())
print("Correlation:", round(books["price"].corr(books["rating"]), 3))
```

Output:

```text
rating
1    33.66
2    34.24
3    34.71
4    32.99
5    32.41
Correlation: -0.032
```

**Line by line.**

- `books.groupby("rating")["price"].mean()` gives one average price for each rating from 1 to 5.
- `.round(2)` rounds to pence; `.to_string()` prints the series without its type line.
- `books["price"].corr(books["rating"])` computes the Pearson correlation: a number between −1 and 1.
- `round(..., 3)` keeps three decimals.

**Reading the result.** The averages stay between £32.41 and £34.71 with no direction: three-star books are the most expensive on average, five-star books the cheapest. The correlation is −0.032, practically zero.

**Checking.** Each rating group is large: 185 to 221 books, so the averages are not driven by a handful of books. The Spearman correlation, which compares the order of values instead of the values themselves, gives −0.033: the same conclusion.

**Mistakes this exercise provokes.**

- Reading the drop from £34.71 to £32.41 as *better books are cheaper*: a difference of about £2 between groups, with a correlation of −0.03, is no link.
- `books.corr()` on the whole table: it fails on the text columns, or needs `numeric_only=True`.
- Concluding that rating does not matter at all: correlation measures only a straight-line link.

**The choice it makes.** A correlation near 0 means no linear link: in this invented catalogue, ratings and prices were drawn independently. On a real shop, a result like this tells you that price is not a signal of quality, which is worth knowing before you build anything on it. Show the group averages beside the single number: readers trust a table they can read more than a coefficient.

**Another way to solve it.** Look before you compute: draw the average price per rating as a bar chart.

```python
import matplotlib.pyplot as plt

books.groupby("rating")["price"].mean().plot.bar()
plt.ylabel("Average price (£)")
plt.savefig("output/ch23/rating_price.png", dpi=150, bbox_inches="tight")
```

Five bars of almost equal height. A chart makes *no link* obvious to a reader who does not know what a correlation is.

**A variation to try.** Repeat the analysis with the number of pages instead of the rating: `books["price"].corr(books["pages"])`. Then group the pages into bands with `pd.cut(books["pages"], [0, 200, 400, 800])` and average the prices per band.

**If your output differs.**

1. **Ratings shown as text** (`'5'`): the column was stored as text; convert with `astype(int)`.
2. **A correlation of `nan`**: one of the columns is empty or constant; print `books[["price", "rating"]].describe()`.

---

## Exercise 23.3 (medium)

> Find the books whose title appears more than once in the catalogue (different books with the same title). Print how many titles are shared and the first one. Expected output:

**What the question asks.** Check whether titles identify books: count the titles used by more than one book, and show the first one if any exist.

**The plan.** Count how many times each title appears with `value_counts`; keep the counts above 1; print how many there are and, if any, the first.

```python
import pandas as pd

books = pd.read_excel("output/ch23/catalogue.xlsx", sheet_name="Catalogue")
counts = books["title"].value_counts()
shared = counts[counts > 1]
print(len(shared), "shared titles")
if len(shared):
    print(shared.index[0], shared.iloc[0])
```

Output:

```text
0 shared titles
```

**Line by line.**

- `books["title"].value_counts()` returns a series: each title, with the number of rows that have it, largest counts first.
- `counts[counts > 1]` keeps the titles that appear at least twice.
- `len(shared)` is the number of shared titles.
- `if len(shared):` prints the first shared title and its count only when there is one; `shared.index[0]` is the title, `shared.iloc[0]` its count.

**Reading the result.** `0 shared titles`: in this catalogue, every one of the 1,000 books has its own title.

**Checking.** `books["title"].duplicated().sum()` also returns 0. Normalise the titles (`str.lower().str.strip()`) and count again: still 0, so no title differs only by capitals or spaces.

**Mistakes this exercise provokes.**

- `print(shared.index[0])` without the `if`: on this catalogue it raises `IndexError`, because `shared` is empty.
- `books.duplicated().sum()`: that looks for whole rows that are identical, a different question.
- Concluding that titles are a safe key on every site: the result holds for this catalogue on this day.

**The choice it makes.** This is why the comparison in `compare.py` is safe only when titles are unique, and why identifiers (the address, the `data-id`, the UPC) are better keys than titles. Check uniqueness before you join on a column. The `if` makes the program correct for both answers, which is what an exercise with an unknown answer requires.

**Another way to solve it.** Check uniqueness in one line, as an assertion inside a pipeline:

```python
assert books["title"].is_unique, "titles are not unique: do not join on them"
```

`is_unique` is `True` here. Put such assertions before every join: when the site adds a second book with an existing title, the program stops with a clear message instead of silently doubling rows.

**A variation to try.** See what a duplicated key does to a join. Add a copy of the first book with a different price, `extra = pd.concat([books, books.head(1).assign(price=1.0)])`, and merge it with the original on `title`: the merged table has 1,001 rows, and that title now has two prices. Then check `extra["url"].is_unique`: `False`, because the copy kept its address. The address, the key the site itself uses, reveals the duplicate.

**If your output differs.**

1. **`IndexError: index 0 is out of bounds`**: the `if len(shared):` is missing.
2. **A positive number**: you read another file, such as a method's CSV with fewer columns; check the path and the sheet.

---

## Exercise 23.4 (thinking)

> You must track the prices of the 1,000 books every day for a month. Which method do you choose, and why? What would make you choose another?

**What the question asks.** A design decision, not code: you must collect 1,000 prices every day for a month. Choose among the four methods of the chapter, justify the choice with numbers, and say what would change it.

**The plan.** Start from the field you need (price), find the cheapest page type that shows it, count requests and minimum time per day and per month, then list the conditions under which another method wins.

**The answer.** Method 1, the 50 list pages: the price is on the list pages, so 50 requests a day (10 seconds of minimum time) are enough, against 1,000 for the detail pages. Store each day's prices with the date (Chapter 22).

**Reading the numbers.** Over 30 days, method 1 sends 1,500 requests; method 2 or 4 would send 30,000, twenty times more load on the site for the same prices. Method 3 sends about twice as many requests as method 1 and needs a browser.

**Checking the answer.** Run `compare.py`: all four methods agree on every price, so the cheapest method loses nothing for this question. Check also that the list pages show the price you need (the current price, not a crossed-out one).

**Mistakes this question provokes.**

- Choosing Scrapy *because it is the professional tool*: it shortens the code, not the minimum time, and it still sends 1,000 requests if you point it at detail pages.
- Choosing the browser because it *sees what a person sees*: the prices are in the HTML source.
- Forgetting the date column: a month of prices without dates cannot be compared.

**The choice it makes.** Choose method 2 or 4 when you also need fields that only the detail pages have, such as the exact stock, and then Scrapy for its speed and robustness. Choose a browser only if the site starts drawing its prices with JavaScript, after looking for a hidden API. A middle path: list pages daily, detail pages once a week for the extra fields.

**Another way to solve it.** Write the decision as a table before choosing, the way the chapter's plan does:

| Need | Pages | Requests a day | Minimum time |
|---|---|---|---|
| Price only | 50 list pages | 50 | 10 s |
| Price and exact stock | 1,000 detail pages | 1,000 | 200 s |

The table makes the cost of each extra field visible: the exact stock costs 950 requests a day.

**A variation to try.** Implement the daily collection with method 1 and Chapter 22's `save_day`, storing `title`, `price` and the day in `output/ch23/prices.db`. Run it twice on the same day and check that the table still has 1,000 rows for that day: the second run replaces the day's rows instead of adding them.

**If your answer differs.** Another method is right when your question differs: if you need the stock every day, method 1 cannot answer it, and the choice is between methods 2 and 4. The reasoning, not the method, is the answer to give.
