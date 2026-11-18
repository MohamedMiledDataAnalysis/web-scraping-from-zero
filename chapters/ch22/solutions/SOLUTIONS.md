# Chapter 22 — detailed solutions

These are the solutions printed in the book, word for word: what the question asks, the plan, the code, line by line, reading the result, checking, the mistakes the exercise provokes, the choice it makes, another way to solve it, a variation to try, and what to do if your output differs. Here, each program is followed by its exact output.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 22.1 (easy)

> Using `history.py`, store the jobs of 1 and 10 March 2027 in a new database `output/ch22/ex1.db`, and print the number of new and removed jobs on the 10th. Expected output:

**What the question asks.** Use the history module on two days that are nine days apart: store each day's jobs in a fresh database, then let `compare` count what changed between them.

**The plan.** Delete any old `ex1.db`; for each of the two days, collect the jobs and save them; call `compare` on the second day and print the lengths of the two tables it returns.

```python
import logging
import sys
from pathlib import Path

sys.path.insert(0, "chapters/ch22/examples")
logging.getLogger("polite").setLevel(logging.WARNING)
import daily_jobs  # noqa: E402
from history import compare, save_day  # noqa: E402

db = "output/ch22/ex1.db"
Path(db).parent.mkdir(parents=True, exist_ok=True)
Path(db).unlink(missing_ok=True)
for day in ["2027-03-01", "2027-03-10"]:
    save_day(db, day, daily_jobs.collect(day))
new, removed = compare(db, "2027-03-10")
print(len(new), "new,", len(removed), "removed")
```

Output:

```text
22 new, 14 removed
```

**Line by line.**

- `sys.path.insert(0, "chapters/ch22/examples")` lets Python import `daily_jobs` and `history` from the examples folder.
- `logging.getLogger("polite").setLevel(logging.WARNING)` silences the client's information messages.
- `Path(db).parent.mkdir(...)` creates `output/ch22` if needed; `Path(db).unlink(missing_ok=True)` deletes the old database, so every run starts from nothing.
- `daily_jobs.collect(day)` reads every page of the board for that day and returns a list of dictionaries.
- `save_day(db, day, ...)` stores them, one row per job, with the day added.
- `compare(db, "2027-03-10")` returns two DataFrames: jobs present on the 10th but not on the previous stored day, and the reverse.

**Reading the result.** `22 new, 14 removed`: between 1 and 10 March, 22 jobs appeared and 14 disappeared.

**Checking.** The board shows 50 jobs on 1 March; 50 + 22 − 14 = 58, which must be the number of jobs on 10 March: `len(daily_jobs.collect("2027-03-10"))` gives 58.

**Mistakes this exercise provokes.**

- Saving into `jobs.db` instead of a new file: the five days of the chapter sit between the 1st and the 10th, and `compare` compares with the 6th instead.
- Forgetting the `unlink`: harmless here, because `save_day` replaces a day already stored; but with other days left in an old file, the previous stored day may not be the 1st.
- Reading `new` as *new since yesterday*: it means *new since the previous day in the database*.

**The choice it makes.** `compare` compares with the **previous stored** day, whatever the gap: here nine days, so the changes are larger than from one day to the next. A job that appeared on the 3rd and vanished on the 8th is invisible to this comparison. Collect every day when the in-between matters.

**Another way to solve it.** Compare the two days with SQL instead of pandas: the new jobs are the ids of the 10th that are not among the ids of the 1st.

```python
import sqlite3

with sqlite3.connect("output/ch22/ex1.db") as con:
    new = con.execute(
        "SELECT COUNT(*) FROM jobs WHERE day = '2027-03-10' AND id NOT IN "
        "(SELECT id FROM jobs WHERE day = '2027-03-01')").fetchone()[0]
print(new)
```

It prints 22. Swap the two dates to count the removed jobs: 14. SQL does the work inside the database, which matters when the table grows to millions of rows.

**A variation to try.** In `jobs.db` (the six consecutive days of the chapter), call `compare` for each day from the 2nd to the 6th. The daily changes are small: 4 new and 1 removed on the 2nd, 2 and 2 on the 3rd, none on the 4th, 3 and 1 on the 5th, 4 and 1 on the 6th.

**If your output differs.**

1. **`ModuleNotFoundError: No module named 'history'`**: run from the repository folder.
2. **`50 new, 0 removed`**: only one day is stored; the first `save_day` failed or used another file name.

---

## Exercise 22.2 (medium)

> After `five_days.py` and `alert_new_jobs.py` (which added 6 March), query `output/ch22/jobs.db` with SQL to print the number of jobs per day. Expected output:

**What the question asks.** One SQL query on the history table: how many rows (jobs) each stored day has.

**The plan.** `GROUP BY day` makes one group per day; `COUNT(*)` counts its rows; `ORDER BY day` sorts the days. pandas runs the query and prints the table.

```python
import sqlite3

import pandas as pd

with sqlite3.connect("output/ch22/jobs.db") as db:
    print(
        pd.read_sql(
            "SELECT day, COUNT(*) AS jobs FROM jobs "
            "GROUP BY day ORDER BY day",
            db,
        ).to_string(index=False)
    )
```

Output:

```text
       day  jobs
2027-03-01    50
2027-03-02    53
2027-03-03    53
2027-03-04    53
2027-03-05    55
2027-03-06    58
```

**Line by line.**

- `with sqlite3.connect("output/ch22/jobs.db") as db:` opens the database built by `five_days.py` and `alert_new_jobs.py`.
- `SELECT day, COUNT(*) AS jobs` returns the day and the number of rows, named `jobs`.
- `GROUP BY day` gathers the rows of the same day; `ORDER BY day` sorts the dates.
- `pd.read_sql(query, db)` returns the result as a DataFrame; `to_string(index=False)` prints it without the row numbers.

**Reading the result.** 50 jobs on 1 March, 53 from the 2nd to the 4th, 55 on the 5th, 58 on the 6th. The board grows a little each day: more jobs appear than disappear.

**Checking.** The differences match the daily changes: from the 1st to the 2nd, 4 new and 1 removed, so 50 + 4 − 1 = 53. The total of the column is 322, the number of rows in the table: `SELECT COUNT(*) FROM jobs`.

**Mistakes this exercise provokes.**

- `COUNT(id)` instead of `COUNT(*)`: the same result here, because `id` is never empty; `COUNT(column)` skips empty values.
- Forgetting `ORDER BY`: SQLite returns the groups in an order it chooses.
- Running before `alert_new_jobs.py`: only five days appear.

**The choice it makes.** Sorting the dates works because they are stored as text in the `YYYY-MM-DD` format: alphabetical order equals date order. With `1/3/2027` the order would be wrong. Store dates in ISO format.

**Another way to solve it.** Read the whole table into pandas and count there:

```python
with sqlite3.connect("output/ch22/jobs.db") as db:
    jobs = pd.read_sql("SELECT * FROM jobs", db)
print(jobs["day"].value_counts().sort_index())
```

The same counts. Fine for 322 rows; with a large history, let the database count and send back six rows instead of the whole table.

**A variation to try.** Count the jobs per city and per day, in one query: `SELECT day, city, COUNT(*) AS jobs FROM jobs GROUP BY day, city ORDER BY day, city`. Then turn it into a table with one column per city: `.pivot(index="day", columns="city", values="jobs")`.

**If your output differs.**

1. **Only five rows**: `alert_new_jobs.py` has not run; it adds 6 March.
2. **`DatabaseError: no such table: jobs`**: the database path is wrong; a wrong path creates a new, empty database.

---

## Exercise 22.3 (medium)

> Find, in `jobs.db`, the job that stayed online the longest during the six stored days (the most rows), with its number of days. Expected output:

**What the question asks.** Find the job with the most rows in the history (one row per day it was online) and say how many days that is.

**The plan.** Group the rows by job, count them, sort by the count from largest to smallest, keep the first. Because several jobs tie, add sorting rules that make the answer always the same.

```python
import sqlite3

import pandas as pd

query = """
    SELECT id, title, company, COUNT(*) AS days, MIN(day) AS first_seen
    FROM jobs GROUP BY id, title, company
    ORDER BY days DESC, first_seen, id LIMIT 1
"""
with sqlite3.connect("output/ch22/jobs.db") as db:
    print(pd.read_sql(query, db).to_string(index=False))
```

Output:

```text
  id                  title           company  days first_seen
1004 Mid-level Data Analyst Kestrel Insurance     6 2027-03-01
```

**Line by line.**

- `GROUP BY id, title, company` makes one group per job; `title` and `company` are in the group so that they can be shown.
- `COUNT(*) AS days` counts the rows of each job: its days online.
- `MIN(day) AS first_seen` is the first day the job was stored.
- `ORDER BY days DESC, first_seen, id` sorts by days, largest first; ties by first day; remaining ties by id.
- `LIMIT 1` keeps the first row.

**Reading the result.** Job 1004, *Mid-level Data Analyst* at Kestrel Insurance, online all six days from 1 March.

**Checking.** Count the tied jobs: `SELECT COUNT(*) FROM (SELECT id FROM jobs GROUP BY id HAVING COUNT(*) = 6)` returns 45. So 45 of the 63 different jobs seen were online every day; job 1004 is simply the smallest id among them.

**Mistakes this exercise provokes.**

- `ORDER BY days DESC LIMIT 1` alone: SQL may return any of the 45 tied jobs, and the answer can change from one run to the next.
- `GROUP BY title`: two different jobs with the same title would be counted as one.
- `WHERE COUNT(*) = 6`: a condition on a group goes in `HAVING`, after `GROUP BY`; `WHERE` filters rows before grouping.

**The choice it makes.** Every column in `SELECT` is either in `GROUP BY` or computed by a function such as `COUNT`: SQLite tolerates other columns, but other databases refuse them. The tie-breaking rules turn *a* longest job into *the* longest job by a stated rule; tell the reader of your report which rule you used.

**Another way to solve it.** Ask for every job that reaches the maximum, instead of one:

```python
query = """
    SELECT id, title, COUNT(*) AS days FROM jobs GROUP BY id, title
    HAVING COUNT(*) = (SELECT MAX(n) FROM
                       (SELECT COUNT(*) AS n FROM jobs GROUP BY id))
    ORDER BY id
"""
```

It returns the 45 jobs online all six days. This is the honest answer when the question is *which jobs stayed longest*: a single row hides the tie.

**A variation to try.** Find the jobs that lasted the **shortest** time: sort with `ORDER BY days, first_seen, id`. Then count how many jobs appeared after 1 March: `SELECT COUNT(*) FROM (SELECT id FROM jobs GROUP BY id HAVING MIN(day) > '2027-03-01')`.

**If your output differs.**

1. **Another job with 6 days**: the `ORDER BY` lacks `first_seen, id`.
2. **`days` is 5**: the 6th is not stored; run `alert_new_jobs.py`.

---

## Exercise 22.4 (harder)

> Write an alert that sends an email only when a **Leeds** job with a maximum salary of at least £60,000 appears between 2027-03-05 and 2027-03-06, using the test mailbox. Print the email's subject line, or `No alert` if nothing qualifies. Expected output:

**What the question asks.** An alert with a condition: run the daily job for the 5th and the 6th, keep the new jobs of the 6th that are in Leeds with a maximum salary of at least £60,000, and send an email only if there is at least one; print the email's subject, or `No alert`.

**The plan.** Start the test mailbox; run both days with `run`, which also stores them and compares; filter the new jobs with two conditions; send the alert with `send_alert`; read the last saved email and print its `Subject:` line. Stop the mailbox in `finally`.

```python
import logging
import sys
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, "chapters/ch22/examples")
logging.getLogger("polite").setLevel(logging.WARNING)
from alert import send_alert  # noqa: E402
from daily_jobs import run  # noqa: E402
from toolkit.mailbox import start_test_mailbox  # noqa: E402

Path("output/ch22").mkdir(parents=True, exist_ok=True)
box = start_test_mailbox(quiet=True)
try:
    run("2027-03-05")
    new, _ = run("2027-03-06")
    hits = new[(new["city"] == "Leeds") & (new["salary_max"] >= 60000)]
    if len(hits):
        send_alert(
            f"Leeds: {len(hits)} well-paid new job(s)",
            "\n".join(
                f"{r.title} at {r.company}" for r in hits.itertuples()
            ),
        )
        text = sorted(Path("output/mailbox").glob("*.eml"))[
            -1
        ].read_text(encoding="utf-8")
        print(
            next(
                l for l in text.splitlines() if l.startswith("Subject:")
            )
        )
    else:
        print("No alert")
finally:
    box.stop()
```

Output:

```text
Subject: Leeds: 1 well-paid new job(s)
```

**Line by line.**

- `start_test_mailbox(quiet=True)` starts a local mail server on port 1025 that saves every email in `output/mailbox`.
- `run("2027-03-05")` collects and stores the 5th; `new, _ = run("2027-03-06")` stores the 6th and keeps the new jobs.
- `new[(new["city"] == "Leeds") & (new["salary_max"] >= 60000)]` keeps the rows where both conditions are true; each condition is in brackets because `&` binds before `==`.
- `if len(hits):` an empty table has length 0, which counts as false.
- The body joins one line per job with `"\n".join(...)`; `itertuples()` gives each row with its columns as attributes.
- `sorted(Path("output/mailbox").glob("*.eml"))[-1]` is the latest email, thanks to the numbered names.
- `next(l for l in ... if l.startswith("Subject:"))` returns the first line that starts with `Subject:`.
- `finally: box.stop()` stops the mailbox even when an error occurs.

**Reading the result.** `Subject: Leeds: 1 well-paid new job(s)`. One new job of the 6th qualifies: the Senior Structured Finance Analyst in Leeds, up to £76,000.

**Checking.** Print `new[["city", "salary_max", "title"]]`: four new jobs on the 6th. A second Leeds job, Junior Business Analyst, pays up to £50,000 and is rightly excluded. Lower the threshold to 50,000: the subject says 2 jobs.

**Mistakes this exercise provokes.**

- `new["city"] == "Leeds" & new["salary_max"] >= 60000` without brackets: Python evaluates `"Leeds" & new["salary_max"]` first and raises `TypeError`.
- `and` instead of `&`: `ValueError: The truth value of a Series is ambiguous`.
- Sending the email before checking `len(hits)`: an alert with nothing in it every day teaches people to ignore alerts.

**The choice it makes.** `run` stores the days in the same `jobs.db` as `five_days.py`; because each day replaces its own rows, running it again does no harm. `_` is the conventional name for a value you do not use. A narrow alert (one city, one salary level) is sent rarely and read every time.

**Another way to solve it.** Write the filter with `query`, which reads like a sentence:

```python
hits = new.query("city == 'Leeds' and salary_max >= 60000")
```

The same row. Inside `query`, `and` is allowed, and brackets are not needed. Use the bracket form when the column names contain spaces or when the conditions are built by code.

**A variation to try.** Put the conditions in a settings dictionary, `rules = {"city": "Leeds", "min_salary": 60000}`, and build the filter from it. Then add a second rule set for Manchester at £70,000, and send one email listing the hits of each rule: on the 6th, the Senior BI Developer in Manchester (up to £78,000) joins the Leeds job.

**If your output differs.**

1. **`No alert`**: the 5th and 6th are compared with other days; check that `run` stores into `output/ch22/jobs.db` and that the 5th ran first.
2. **`ConnectionRefusedError`**: the mailbox did not start, or port 1025 is used by another program.
3. **`StopIteration`**: the email has no `Subject:` line; open the `.eml` file.
