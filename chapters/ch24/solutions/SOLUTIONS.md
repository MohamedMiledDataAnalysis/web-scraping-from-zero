# Chapter 24 — detailed solutions

These are the solutions printed in the book, word for word: what the question asks, the plan, the code, line by line, reading the result, checking, the mistakes the exercise provokes, the choice it makes, another way to solve it, a variation to try, and what to do if your output differs. Here, each program is followed by its exact output.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 24.1 (easy)

> Print the number of jobs in the database per city, largest first. Expected output:

**What the question asks.** One summary of the tracker's database: how many of its jobs are in each city, from the largest count to the smallest.

**The plan.** One SQL query: group the rows by city, count them, sort by the count; pandas runs it and prints the table.

```python
import sqlite3

import pandas as pd

with sqlite3.connect("output/ch24/tracker.db") as db:
    print(
        pd.read_sql(
            "SELECT city, COUNT(*) AS jobs FROM jobs GROUP BY city "
            "ORDER BY jobs DESC, city",
            db,
        ).to_string(index=False)
    )
```

Output:

```text
      city  jobs
     Leeds    12
Manchester     7
    Remote     6
    London     3
```

**Line by line.**

- `sqlite3.connect("output/ch24/tracker.db")` opens the database of the week's run.
- `SELECT city, COUNT(*) AS jobs ... GROUP BY city` gives one row per city with its number of jobs.
- `ORDER BY jobs DESC, city` sorts by count, largest first, and by name when two cities have the same count.
- `pd.read_sql` returns a DataFrame; `to_string(index=False)` prints it without row numbers.

**Reading the result.** Leeds has 12 of the tracked jobs, then Manchester (7), Remote (6) and London (3). Only the four cities of the configuration appear, because the tracker stores only matching jobs.

**Checking.** The counts add up to 28, the number of rows: `SELECT COUNT(*) FROM jobs`. Each job has one row, whatever the number of days it stayed online, so this counts jobs, not job-days.

**Mistakes this exercise provokes.**

- `ORDER BY COUNT(*) DESC` works too; `ORDER BY jobs DESC` uses the name given with `AS`, which is easier to read.
- Running it on `output/ch22/jobs.db`: that table has one row per job **per day**, so the counts are about six times larger.
- Expecting Edinburgh or Paris: they are on the board but not in `config.json`.

**The choice it makes.** The query counts the jobs the tracker kept, not the jobs on the board. That is the right number for *where are my opportunities?*; for *where is the market?*, count the list pages without the city filter.

**Another way to solve it.** Read the table and count with pandas:

```python
with sqlite3.connect("output/ch24/tracker.db") as db:
    jobs = pd.read_sql("SELECT * FROM jobs", db)
print(jobs["city"].value_counts())
```

The same counts. `value_counts` sorts by count but leaves ties in an order of its own; the SQL version breaks ties by name.

**A variation to try.** Add the average maximum salary per city: `SELECT city, COUNT(*) AS jobs, ROUND(AVG(salary_max)) AS avg_max FROM jobs GROUP BY city ORDER BY jobs DESC, city`. Then keep only the cities with at least five jobs, with `HAVING COUNT(*) >= 5`.

**If your output differs.**

1. **`DatabaseError: no such table: jobs`**: the week has not run; run the chapter's `week.py` first.
2. **Larger counts**: you opened Chapter 22's database.

---

## Exercise 24.2 (medium)

> Add `"sql"` to the searches of a copy of the configuration and count, without storing anything, how many matching jobs the board has on 2027-03-07 with and without it. Use `collect_list` and `matches`. Expected output:

**What the question asks.** Measure what one more search word brings, before changing the real configuration: collect the jobs of 7 March for the current searches, then for the searches plus *sql*, and count the matching jobs each time, storing nothing.

**The plan.** Read the configuration; loop over two lists of searches; for each list, merge the results of every search in one dictionary keyed by job id, so that a job found twice counts once; count the jobs that pass `matches`.

```python
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, "chapters/ch24/project")
logging.getLogger("polite").setLevel(logging.WARNING)
from tracker import collect_list, matches  # noqa: E402

config = json.loads(Path("output/ch24/config.json").read_text())
for searches in [config["searches"], config["searches"] + ["sql"]]:
    jobs = {}
    for q in searches:
        jobs.update(collect_list("2027-03-07", q))
    print(
        searches,
        "->",
        sum(matches(j, config) for j in jobs.values()),
        "matching jobs",
    )
```

Output:

```text
['analyst', 'python', 'data'] -> 24 matching jobs
['analyst', 'python', 'data', 'sql'] -> 25 matching jobs
```

**Line by line.**

- `json.loads(Path(...).read_text())` reads the configuration: three searches, four cities, a minimum salary of £40,000.
- `config["searches"] + ["sql"]` makes a **new** list; the configuration itself is not changed.
- `jobs.update(collect_list("2027-03-07", q))` adds the jobs of one search; a job already present is replaced by the same data, so the dictionary never holds duplicates.
- `matches(j, config)` returns `True` or `False`; `sum(...)` counts the `True` values.

**Reading the result.** 24 matching jobs with the three searches, 25 with *sql*: the extra word brings one job, a Junior BI Developer, remote, up to £55,000.

**Checking.** The three searches find 47 different jobs (22 + 16 + 19 results, with overlaps); 23 of them are in Edinburgh, Lyon or Paris, which leaves 24. The *sql* search alone finds 13 jobs, and 12 of them were already found.

**Mistakes this exercise provokes.**

- Adding up the number of results of each search: 22 + 16 + 19 = 57 counts the overlapping jobs twice.
- `config["searches"].append("sql")`: it changes the list in place, so the first loop already includes *sql*.
- Calling `run_day`: it stores the jobs and fetches details, which the exercise forbids.

**The choice it makes.** `sum(...)` of `True` and `False` counts the `True` values. The search on the board matches the title and the skills, so *sql* finds jobs whose title says nothing about data. Each extra search word costs list pages every day (here one or two more requests) for one more job: measure before you add.

**Another way to solve it.** Use sets of ids, which make the difference explicit:

```python
before = {i for q in config["searches"]
          for i, j in collect_list("2027-03-07", q).items() if matches(j, config)}
extra = {i for i, j in collect_list("2027-03-07", "sql").items() if matches(j, config)}
print(len(before), len(before | extra), extra - before)
```

`before | extra` is the union, `extra - before` the jobs only *sql* brings: `{1323}`. It sends the same requests and also tells you **which** jobs are new.

**A variation to try.** Try other words in place of *sql*, such as *excel* or *finance*, and print the number of extra matching jobs and extra list pages for each. Keep the words that bring at least one job a week.

**If your output differs.**

1. **25 on the first line**: `append` changed the configuration list before the first loop.
2. **More than 25**: you counted every job instead of the matching ones; check `matches`.

---

## Exercise 24.3 (medium)

> From the database, print the jobs that closed during the week, with the number of days each stayed online, counted from the day it was posted. Expected output:

**What the question asks.** Use the dates in the database to find the jobs that disappeared before the last day of the week, and how long each stayed online since it was posted.

**The plan.** A job last seen before 7 March, the last day of the week, was not on the board that day: it closed. Compute its number of days online as `last_seen − posted + 1`, with SQLite's date functions.

```python
import sqlite3

import pandas as pd

query = """
    SELECT title, city, posted, last_seen,
           CAST(julianday(last_seen) - julianday(posted) + 1
                AS INTEGER) AS days
    FROM jobs WHERE last_seen < '2027-03-07' ORDER BY days, title
"""
with sqlite3.connect("output/ch24/tracker.db") as db:
    print(pd.read_sql(query, db).to_string(index=False))
```

Output:

```text
                               title   city     posted  last_seen  days
          Mid-level Business Analyst  Leeds 2027-02-20 2027-03-02    11
        Mid-level Operations Analyst  Leeds 2027-02-19 2027-03-01    11
Mid-level Structured Finance Analyst  Leeds 2027-02-17 2027-03-02    14
             Senior Python Developer London 2027-02-08 2027-03-04    25
```

**Line by line.**

- `WHERE last_seen < '2027-03-07'` keeps the jobs not seen on the last day; text dates in `YYYY-MM-DD` format compare in date order.
- `julianday(last_seen) - julianday(posted)` subtracts two dates as numbers of days.
- `+ 1` counts both ends: a job posted and closed on the same day was online 1 day.
- `CAST(... AS INTEGER)` turns the result into a whole number.
- `ORDER BY days, title` lists the shortest-lived first.

**Reading the result.** Four jobs closed during the week, after 11 to 25 days online: three in Leeds, one in London.

**Checking.** Recompute one by hand: the Mid-level Business Analyst was posted on 20 February and last seen on 2 March; February 2027 has 28 days, so 20 February to 2 March is 10 days later, 11 days counted inclusively. The query agrees.

**Mistakes this exercise provokes.**

- `last_seen - posted` without `julianday`: SQLite subtracts the leading numbers of the text (2027 − 2027) and returns 0.
- `WHERE last_seen < MAX(last_seen)`: an aggregate cannot go in `WHERE`; use the date, or a sub-query.
- Counting from `first_seen`: all four were already online on the first day of tracking, so you would measure only one to four days.

**The choice it makes.** `julianday` turns a date into a decimal number of days, so SQLite can subtract dates; `CAST(... AS INTEGER)` keeps whole days. A daily tracker tells you within a day that a job you wanted is gone. Count from `posted`, not `first_seen`: the tracker only saw the end of their lives. The `+ 1` is a convention; state it next to the numbers.

**Another way to solve it.** Do the date arithmetic in pandas:

```python
with sqlite3.connect("output/ch24/tracker.db") as db:
    jobs = pd.read_sql("SELECT title, city, posted, last_seen FROM jobs", db)
closed = jobs[jobs["last_seen"] < "2027-03-07"].copy()
closed["days"] = (pd.to_datetime(closed["last_seen"])
                  - pd.to_datetime(closed["posted"])).dt.days + 1
print(closed.sort_values(["days", "title"]).to_string(index=False))
```

The same four rows. pandas is easier to read; SQL works without loading the table.

**A variation to try.** For the jobs still open on 7 March, compute how long they have been online so far: the same formula with `'2027-03-07'` in place of `last_seen`, and `WHERE last_seen = '2027-03-07'`. The oldest open job tells you how long a job can stay on this board.

**If your output differs.**

1. **`days` is 0 everywhere**: `julianday` is missing.
2. **No rows**: the week has not run up to 7 March, so `last_seen` never reaches it; check `SELECT MAX(last_seen) FROM jobs`.

---

## Exercise 24.4 (harder)

> Count the requests the week sent: list pages and detail pages. Wrap `client.get` to count calls, run the week again quietly without emails, and print the totals. Expected output:

**What the question asks.** Measure the load the tracker puts on the site over a week: run the seven days again into a separate database, without emails, and count every request by type.

**The plan.** Replace the client's `get` method with a function that counts the call, then calls the original. List pages and detail pages are told apart by their address. Run the seven days, then print the counts.

```python
import datetime as dt
import json
import logging
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, "chapters/ch24/project")
logging.getLogger("polite").setLevel(logging.WARNING)
import tracker  # noqa: E402

counts = Counter()
original_get = tracker.client.get


def counting_get(url, **kwargs):
    counts["detail pages" if "/?day=" in url else "list pages"] += 1
    return original_get(url, **kwargs)


tracker.client.get = counting_get
tracker.DB = "output/ch24/count.db"
Path(tracker.DB).unlink(missing_ok=True)
config = json.loads(Path("output/ch24/config.json").read_text())
for n in range(7):
    tracker.run_day(
        (dt.date(2027, 3, 1) + dt.timedelta(n)).isoformat(),
        config,
        with_email=False,
    )
print(dict(counts), "| total:", sum(counts.values()))
```

Output:

```text
{'list pages': 36, 'detail pages': 28} | total: 64
```

**Line by line.**

- `original_get = tracker.client.get` keeps a reference to the real method before replacing it.
- `counting_get(url, **kwargs)` accepts the same arguments; `**kwargs` passes on `params` and anything else unchanged.
- `"/?day=" in url`: detail addresses are built as `{BASE}{job_id}/?day={day}`; list pages pass their parameters separately, so their `url` is just `BASE`.
- `tracker.client.get = counting_get` installs the wrapper; every call inside `tracker` now goes through it.
- `tracker.DB = "output/ch24/count.db"` and `unlink` give the run a fresh, separate database.
- `dt.date(2027, 3, 1) + dt.timedelta(n)` gives the seven days; `.isoformat()` writes them as `YYYY-MM-DD`.
- `with_email=False` skips the digest.

**Reading the result.** 36 list pages and 28 detail pages: 64 requests for a week, about 9 a day, or under two seconds of polite waiting a day.

**Checking.** 28 is the number of jobs in the tracker's database: the tracker fetches a detail page only for a job it has not seen before, once in its life. Run the solution again: the same totals, because the separate database is deleted first.

**Mistakes this exercise provokes.**

- Replacing `requests.get` instead of `tracker.client.get`: the tracker uses its `PoliteClient`, so nothing is counted.
- A wrapper without `**kwargs`: `collect_list` passes `params=`, and the call fails with `TypeError`.
- Running on the real `tracker.db`: every job is already known, so the count shows 0 detail pages.

**The choice it makes.** Replacing a function by a wrapper that counts and then calls the original is a quick way to measure a program without changing its code. A list page address contains `?q=`, a detail page `/?day=`. Fetching details only for new jobs is what keeps the detail count at 28 instead of one per job per day.

**Another way to solve it.** Count the responses instead of the calls. `PoliteClient` sends its requests through a `requests.Session`, which accepts response hooks: functions called on every response.

```python
def count_response(response, *args, **kwargs):
    counts["detail pages" if "/?day=" in response.url and "q=" not in response.url
           else "list pages"] += 1

tracker.client.session.hooks["response"].append(count_response)
```

The hook sees the final address of every response, parameters included, so the test must exclude `q=`. It counts a retried request once per attempt, which measures the real load on the site; the wrapper counts what the tracker asks for. Neither sees `robots.txt`, which `RobotFileParser` downloads with its own connection.

**A variation to try.** Estimate the cost of the details without the *new jobs only* rule: count the matching jobs per day (the first value `run_day` returns) and add them up over the week. That is the number of detail requests a naive tracker would send.

**If your output differs.**

1. **0 detail pages**: the database was not deleted; check `tracker.DB` and the `unlink`.
2. **Everything counted as list pages**: print one `url` inside the wrapper; your test string does not match.
