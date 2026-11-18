# Chapter 26 — detailed solutions

These are the solutions printed in the book, word for word: what the question asks, the plan, the code, line by line, reading the result, checking, the mistakes the exercise provokes, the choice it makes, another way to solve it, a variation to try, and what to do if your output differs. Here, each program is followed by its exact output.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 26.1 (easy)

> From `library_value.csv`, print the three books with the most pages per pound, with their category. Expected output:

**What the question asks.** Read the dataset the chapter built and list the three books that give the most pages for each pound, with their category.

**The plan.** Read the CSV; keep the three rows with the largest `pages_per_pound`; show the title, category and value.

```python
import pandas as pd

data = pd.read_csv("output/ch26/dataset/library_value.csv")
top = data.nlargest(3, "pages_per_pound")[
    ["title", "category", "pages_per_pound"]
]
print(top.to_string(index=False))
```

Output:

```text
                     title category  pages_per_pound
The Window and the Harbour  Mystery           118.46
        The Crimson Forest  History           118.13
        Mirrors in the Map  Science           117.51
```

**Line by line.**

- `pd.read_csv("output/ch26/dataset/library_value.csv")` reads the 920 books in stock, with `pages_per_pound` already computed.
- `data.nlargest(3, "pages_per_pound")` returns the three rows with the largest values, largest first.
- `[["title", "category", "pages_per_pound"]]` keeps three columns; `to_string(index=False)` prints without row numbers.

**Reading the result.** *The Window and the Harbour* (Mystery) gives 118.46 pages per pound, followed closely by *The Crimson Forest* (History) and *Mirrors in the Map* (Science): three categories, so no single category owns the best deals.

**Checking.** Recompute the first: 693 pages for £5.85 gives 693 / 5.85 = 118.46. The whole column equals `(pages / price).round(2)`. The median book gives 12.56 pages per pound, so these three are about nine times better value than a typical book.

**Mistakes this exercise provokes.**

- `sort_values("pages_per_pound").head(3)`: the three **worst** values, starting at 1.82 pages per pound.
- Reading the original catalogue of Chapter 23 instead: it includes the 80 books out of stock, which the chapter's question excludes.
- Treating *pages per pound* as quality: it measures quantity per pound, nothing else.

**The choice it makes.** The ratio favours long, cheap books: all three have over 600 pages and cost under £6. A ratio is a good first measure because it is simple to explain; state its blind spots in the data dictionary.

**Another way to solve it.** Show the parts of the ratio beside it, so the reader sees why each book ranks high:

```python
cols = ["title", "category", "pages", "price", "pages_per_pound"]
print(data.nlargest(3, "pages_per_pound")[cols].to_string(index=False))
```

The fourth book, *Empty Station*, is close behind at 115.92: print `nlargest(5, ...)` before you call the first three *the best*.

**A variation to try.** Find the best-value book **in each category**: `data.loc[data.groupby("category")["pages_per_pound"].idxmax(), ["category", "title", "pages_per_pound"]]`. A reader who only reads Poetry wants that list, not the overall top three.

**If your output differs.**

1. **`FileNotFoundError`**: the chapter's build step has not run; it writes `output/ch26/dataset/`.
2. **Different titles**: you read a file built from another day or another method; check the README of the dataset for its date.

---

## Exercise 26.2 (medium)

> Answer a second question with the same dataset: *does a newer book give fewer pages per pound?* Print the median pages per pound of books published before 1990, from 1990 to 2009, and from 2010, with the number of books in each band. Use `pd.cut(data["year"], bins=[1900, 1989, 2009, 2100], labels=[...])`. Expected output:

**What the question asks.** Reuse the same dataset for a second question: do newer books give fewer pages per pound? Put each book in one of three periods by publication year and compare the median of each period, with its number of books.

**The plan.** Create a `period` column with `pd.cut`; group by period; compute the count and the median of `pages_per_pound`; round and print.

```python
import pandas as pd

data = pd.read_csv("output/ch26/dataset/library_value.csv")
data["period"] = pd.cut(data["year"], bins=[1900, 1989, 2009, 2100],
                        labels=["before 1990", "1990-2009", "2010 on"])
print(data.groupby("period", observed=True)["pages_per_pound"]
          .agg(["count", "median"]).round(1).to_string())
```

Output:

```text
             count  median
period                    
before 1990    468    12.8
1990-2009      253    12.4
2010 on        199    12.4
```

**Line by line.**

- `pd.cut(data["year"], bins=[1900, 1989, 2009, 2100], labels=[...])` puts each year in a band: (1900, 1989], (1989, 2009], (2009, 2100]. Each band includes its upper limit, so 1989 is *before 1990* and 1990 starts the second band.
- The labels give the bands readable names, in the same order as the bands.
- `groupby("period", observed=True)` groups by band; `observed=True` keeps only the bands that have books.
- `.agg(["count", "median"])` computes both per band; `.round(1)` keeps one decimal.

**Reading the result.** The medians are 12.8, 12.4 and 12.4 pages per pound: the period makes no clear difference. The bands are unequal (468, 253 and 199 books), but all are large enough for a median.

**Checking.** The counts add up to 920, so every book falls in a band: the years run from 1952 to 2026, inside the limits. The correlation between year and pages per pound is 0.01, which confirms *no link*.

**Mistakes this exercise provokes.**

- `bins=[1900, 1990, 2010, 2100]`: 1990 then falls in the **first** band and 2010 in the second, so the counts change (482, 255, 183) and the labels lie.
- Fewer labels than bands: `ValueError`; `pd.cut` needs exactly one label per band.
- Comparing means: a few very cheap long books pull a mean up, which is why the chapter uses medians.

**The choice it makes.** `pd.cut` puts each year in a band: `bins` gives the limits (each band includes its upper limit), `labels` the band names. In this invented library, the period makes no clear difference; on real data, check whether the bands hold enough books before you compare their medians. Equal-width periods are easy to explain; `pd.qcut(data["year"], 3)` makes bands with equal numbers of books instead (311, 310 and 299 here), which compares like with like but gives odd limits.

**Another way to solve it.** Skip the bands and measure the link directly:

```python
print(round(data["year"].corr(data["pages_per_pound"]), 3))
print(round(data["year"].corr(data["pages_per_pound"], method="spearman"), 3))
```

0.01 and 0.001: no link, linear or by rank. The bands make the result readable for anyone; the correlation is one number for a reader who knows what it means. Give the table in a report and the correlation in its notes.

**A variation to try.** Cross the two questions: the median pages per pound per category **and** period, with `data.pivot_table(index="category", columns="period", values="pages_per_pound", aggfunc="median", observed=True)`. Look at the number of books per cell first: a median over three books says little.

**If your output differs.**

1. **Counts that add up to less than 920**: some years fall outside `bins`; the rows get `NaN` and drop out of the groups.
2. **A band with a count of 0 and `NaN` as median**: `observed=False` keeps empty bands; with `observed=True` they disappear. Here every band has books, so both give the same table.

---

## Exercise 26.3 (project)

> Fill in the plan template for a question of your own, up to section 5, before writing any code. Ask someone else to read it: if they cannot tell what number will answer your question, rewrite section 1.

**What the question asks.** Plan before you code: fill in sections 1 to 5 of the template for your own question, then test the plan on a reader. The test is section 1: a stranger must be able to say which number will answer it.

**The plan.** Write the question as one sentence ending in a measurable quantity. Then fill each section in order, because each answer depends on the previous one: the rules decide the method, the method decides the budget, the fields decide the checks.

**A model answer, on the Practice Ground.** Here is the template filled in for a question on the job board:

```text
## 1. Question
Which city on the job board has the highest median maximum salary
on 1 March 2027?

## 2. Sources and rules (date: 2027-03-01)
- Official API or download?   no
- Terms: scraping allowed for learning; 0.2 s between requests;
  no /private/ or /admin/
- robots.txt for /jobs/: allowed for every robot
- Personal data?   no (invented companies, no names)
- What I will do with the data: learning
- Licence of the data I will publish: none; all data is invented

## 3. Method and budget
- Decision chart answer: method 3 (data in the page source)
- Pages to fetch: 4 list pages (50 jobs, 15 per page)
  Delay (s): 0.2     Minimum time: under 1 s

## 4. Fields
| city       | p.location on each li.job | text           |
| salary_max | p.salary, after the dash  | integer pounds |
| id         | data-id of li.job         | integer        |

## 5. Checks
- Count expected: 50 jobs, ids unique
- Fields never empty: city, salary_max
- Value ranges: salary_max between 15,000 and 300,000
```

**Reading the plan.** A reader can name the answer: a city and a median salary in pounds. The plan also shows what is not needed: no detail pages, because city and salary are on the list.

**Checking the plan.** Each check traces back to a field or to the source: 50 jobs is what the board shows on that day; the unique ids catch a pager loop (Chapter 22); the salary range catches a parsing error such as reading the minimum or a value in pence.

**Mistakes this exercise provokes.**

- A question such as *analyse the job market*: nobody can tell which number answers it, so nothing tells you when you are done.
- Filling section 3 before section 2: the method depends on whether an official API or download exists and on what the terms allow.
- Checks that only say *data looks fine*: write numbers a program can test.

**The choice it makes.** The plan takes ten minutes and saves the hours spent collecting fields you do not need. Rewrite section 1 until the reader's guess matches yours; everything else follows from it.

**Another way to solve it.** Write the plan as a Python dictionary, as the chapter's `plan.py` does, instead of a Markdown file. The checks then become code you can run later:

```python
plan = {"question": "Which city has the highest median maximum salary on 2027-03-01?",
        "expected_rows": 50, "never_empty": ["city", "salary_max"],
        "salary_range": (15000, 300000)}
```

The Markdown template is easier for another person to read; the dictionary is easier for your program to use. Many projects keep both: the plan for people, the checks in code.

**A variation to try.** Swap the question for one that needs detail pages, such as *which skill appears most often in Leeds jobs?*. Redo sections 3 to 5: the skills are only on the detail pages, so the budget grows from 4 requests to 4 plus one per Leeds job, and the checks gain *skills never empty*.

**If your answer differs.** Your plan will differ: it is your question. Test it with the reader's guess, and check that every field in section 4 is needed by section 1 and every check in section 5 can be run by code.
