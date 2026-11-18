# Chapter 20 — detailed solutions

These are the long versions of the solutions printed in the book. Each has the same parts as the book, with more detail, plus parts the book has no room for: another way to solve the exercise, a variation to try, and what to do if your output differs.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 20.1 (easy)

> Use `get_with_retries` from `backoff.py` (copy the function) on `/trouble/status/500` with 3 tries and `base_wait=0.2`, and catch the final error to print its message. Expected output:

**What the question asks.** See the retry function give up: a page that always answers 500, three tries with short waits, and the final error caught and printed instead of crashing the program.

**The plan.** Copy `get_with_retries` from `backoff.py`; call it on `/trouble/status/500` with `tries=3` and `base_wait=0.2`; wrap the call in `try` and print the `RuntimeError` message.

```python
import time

import requests

RETRY_STATUS = {429, 500, 502, 503, 504}
session = requests.Session()


def get_with_retries(url, tries=4, base_wait=0.5):
    for attempt in range(1, tries + 1):
        try:
            r = session.get(url, timeout=10)
        except (requests.Timeout, requests.ConnectionError) as error:
            reason = type(error).__name__
        else:
            if r.status_code not in RETRY_STATUS:
                return r
            reason = f"status {r.status_code}"
        if attempt == tries:
            raise RuntimeError(
                f"Gave up after {tries} tries: {url} ({reason})"
            )
        time.sleep(base_wait * 2 ** (attempt - 1))


try:
    get_with_retries(
        "http://localhost:8000/trouble/status/500",
        tries=3,
        base_wait=0.2,
    )
except RuntimeError as error:
    print(error)
```

Output:

```text
Gave up after 3 tries: http://localhost:8000/trouble/status/500 (status 500)
```

**Line by line.**

- `RETRY_STATUS` lists the codes worth retrying: 429 and the server errors.
- `for attempt in range(1, tries + 1):` numbers the attempts 1, 2, 3.
- `except (requests.Timeout, requests.ConnectionError)` catches network failures and records their name as the reason.
- The `else:` block runs only when the request itself worked: a status outside `RETRY_STATUS` is returned at once; a retryable status becomes the reason.
- `if attempt == tries:` on the last attempt, raise `RuntimeError` with a message naming the address and the reason.
- `time.sleep(base_wait * 2 ** (attempt - 1))` waits 0.2 s, then 0.4 s: the wait doubles each time (*exponential backoff*).

**Reading the result.** `Gave up after 3 tries: http://localhost:8000/trouble/status/500 (status 500)`. The program ends normally, with a message that says what failed and why.

**Checking.** The whole call takes about 0.6 seconds: three requests and two waits (0.2 + 0.4). Change the address to `/trouble/status/404`: the function returns the response at once, because 404 is not worth retrying.

**Mistakes this exercise provokes.**

- Retrying every status, 404 included: a page that does not exist will never appear, and the scraper wastes time.
- A fixed wait between tries: on a busy server, a doubling wait gives it room to recover.
- `while True:` with no limit on tries: a permanent error loops for ever.

**The choice it makes.** A permanent 500 is requested three times (two retries), then the function gives up with a clear message instead of looping forever. Giving up is part of being polite: the server is broken, and hammering it will not fix it.

### Another way to solve it

`requests` can retry by itself through `urllib3`'s `Retry`, attached to a session:

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
session.mount("http://", HTTPAdapter(max_retries=Retry(
    total=2, backoff_factor=0.2, status_forcelist=[500, 502, 503, 504])))
try:
    session.get("http://localhost:8000/trouble/status/500", timeout=10)
except requests.exceptions.RetryError as error:
    print("RetryError", error)
```

`total=2` means two retries, so three requests, as above. It is less code, but the retries happen out of sight: no log line tells you they took place. The book's function, and `PoliteClient`, log each retry.

### A variation to try

Count the waits: add `print(f"attempt {attempt} failed ({reason})")` before the `sleep`. With `tries=5` you see the waits 0.2, 0.4, 0.8 and 1.6 seconds, and the call takes about 3 seconds.

### If your output differs

1. **The program stops with a traceback**: the call is not inside `try`/`except RuntimeError`.
2. **It waits much longer**: `base_wait` is still the default 0.5; pass `base_wait=0.2`.

---

## Exercise 20.2 (medium)

> Use `PoliteClient` with `timeout=1` and `tries=2` on `/trouble/slow?seconds=2`. Catch the error and print it. Expected output:

**What the question asks.** See `PoliteClient` handle a page slower than the time you allow: with a 1-second timeout and 2 tries, a page that takes 2 seconds fails twice, and the client logs what it did before giving up.

**The plan.** Configure logging to print levels and messages to the screen; create the client with `timeout=1`, `tries=2`, a short `base_wait`; request the slow page; catch and print the `RuntimeError`.

```python
import logging
import sys

sys.path.insert(0, ".")
from toolkit.polite import PoliteClient  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-7s %(message)s",
    stream=sys.stdout,
)
client = PoliteClient(
    "LearningScraper/1.0", delay=0.2, timeout=1, tries=2, base_wait=0.2
)
try:
    client.get("http://localhost:8000/trouble/slow?seconds=2")
except RuntimeError as error:
    print(error)
```

Output:

```text
WARNING ReadTimeout on http://localhost:8000/trouble/slow?seconds=2, retry 1 in 0.2 s
ERROR   Gave up on http://localhost:8000/trouble/slow?seconds=2 after 2 tries (ReadTimeout)
Gave up on http://localhost:8000/trouble/slow?seconds=2 (ReadTimeout)
```

**Line by line.**

- `sys.path.insert(0, ".")` lets Python find the `toolkit` folder of the repository, so that `from toolkit.polite import PoliteClient` works.
- `logging.basicConfig(...)` sets the log: messages of level `INFO` and above, formatted as the level padded to 7 characters (`%(levelname)-7s`) then the message, written to `sys.stdout`.
- `PoliteClient("LearningScraper/1.0", delay=0.2, timeout=1, tries=2, base_wait=0.2)` names the robot, waits 0.2 s between requests, gives up on any request after 1 second, and tries twice.
- `client.get(...)` raises `RuntimeError` after the last failed try; `print(error)` shows its message.

**Reading the result.** Three lines. A `WARNING` for the first timeout and the planned retry; an `ERROR` when the client gives up after two tries; then your `print` of the error message.

**Checking.** Raise the timeout to 3 seconds: the page arrives on the first try, and nothing is logged at warning level. Ask for `/trouble/slow?seconds=0`: instant.

**Mistakes this exercise provokes.**

- No `logging.basicConfig`: Python still prints the warning and the error through a last-resort handler, but on the error stream and without your format, and `INFO` messages are not shown at all.
- Catching `requests.Timeout` around `client.get`: the client already catches it and raises `RuntimeError` at the end.
- Running the script from inside `chapters/ch20/solutions/`: `ModuleNotFoundError: No module named 'toolkit'`. Run from the repository folder.

**The choice it makes.** The client logs the retry and the final failure, then raises the error that the program prints. `stream=sys.stdout` sends the log to the same place as `print`; by default, logging writes to the error stream, which the terminal also shows. Configure logging in every real scraper.

### Another way to solve it

`requests` accepts two timeouts, one to connect and one to wait for the answer:

```python
requests.get("http://localhost:8000/trouble/slow?seconds=2", timeout=(3, 1))
```

It raises `requests.ReadTimeout`: the connection was quick, the answer too slow. A short connect timeout catches a site that is down; a longer read timeout lets a slow page finish. `PoliteClient` passes one value for both.

### A variation to try

Show the difference between a refusal and a failure: request `/trouble/status/403` with the client. It raises `NotAllowed: status 403 for http://localhost:8000/trouble/status/403` at once, with no retry, because a refusal will not change. A 404 is simply returned: `client.get(".../trouble/status/404").status_code` is 404.

### If your output differs

1. **Only the last line**: logging is not configured; check `basicConfig`.
2. **`ModuleNotFoundError: No module named 'toolkit'`**: run from the repository folder.
3. **The page arrives**: the timeout is larger than 2 seconds.

---

## Exercise 20.3 (medium)

> Scrape pages 1 to 5 of the library with `PoliteClient`, build a DataFrame of titles and prices, and run `check_books` on it with `expected_rows=100`. Then run the same check on a version where you break the price selector on purpose. Expected output:

**What the question asks.** Prove that automatic checks catch what errors do not: scrape 100 books correctly and check them (no problem), then scrape with a broken price selector and check again (the problem appears).

**The plan.** One function `scrape(price_selector)` that reads pages 1 to 5 and returns a DataFrame, writing `None` when the price element is missing. Call `check_books` on both results.

```python
import sys

import pandas as pd
from bs4 import BeautifulSoup

sys.path.insert(0, ".")
sys.path.insert(0, "chapters/ch20/examples")
from checks import check_books  # noqa: E402
from toolkit.polite import PoliteClient  # noqa: E402

client = PoliteClient("LearningScraper/1.0", delay=0.2)


def scrape(price_selector):
    rows = []
    for page in range(1, 6):
        html = client.get(
            f"http://localhost:8000/library/page-{page}.html"
        ).text
        for card in BeautifulSoup(html, "html.parser").select(
            "article.book-card"
        ):
            price = card.select_one(price_selector)
            rows.append(
                {
                    "title": card.select_one("h3 a")["title"],
                    "price": float(price.text[1:]) if price else None,
                }
            )
    return pd.DataFrame(rows)


print(check_books(scrape("p.price"), expected_rows=100))
print(check_books(scrape("p.cost"), expected_rows=100))
```

Output:

```text
[]
['price: 100% missing']
```

**Line by line.**

- Two `sys.path.insert` lines let Python find `toolkit` and the `checks.py` file of the examples folder.
- `scrape(price_selector)` takes the selector as a parameter, so one function produces both versions.
- `price = card.select_one(price_selector)` is `None` when the selector matches nothing; `float(price.text[1:]) if price else None` records a missing price instead of crashing.
- `check_books(df, expected_rows=100)` returns a list of problems; an empty list means *all good*.
- `p.cost` is the deliberately wrong selector: no element has that class.

**Reading the result.** `[]` for the correct scrape: 100 rows, no missing prices. `['price: 100% missing']` for the broken one. Both scrapes ran without any error.

**Checking.** Print `scrape("p.cost").head()`: 100 rows, titles present, every price `None`. Change `expected_rows` to 120: the first check now reports `100 rows instead of 120`.

**Mistakes this exercise provokes.**

- `float(card.select_one(price_selector).text[1:])` without the `if`: the broken selector crashes with `AttributeError` instead of producing the silent failure the exercise is about.
- Checking only `len(df) > 0`: both versions pass.
- Running `checks.py`'s own tests by accident: they stay silent, thanks to `if __name__ == "__main__":`.

**The choice it makes.** With the wrong selector, the program produces 100 rows without any error; only the check reveals that every price is missing. A strict check (`expected_rows=100`) catches more problems but fails when the site legitimately changes; a loose one (more than 0 rows) never fails wrongly but misses partial losses. Use what the site announces (*1000 results*) when it announces something.

### Another way to solve it

Make the check fail loudly instead of returning a list, so that a nightly job stops:

```python
problems = check_books(df, expected_rows=100)
if problems:
    raise RuntimeError("Checks failed: " + "; ".join(problems))
```

Returning a list lets you decide; raising guarantees nobody uses bad data by mistake. Chapter 22's unattended job raises.

### A variation to try

See the 5% threshold of `check_books` at work. A DataFrame of 100 books with 4 missing prices passes (`[]`); with 6 missing prices it fails with `['price: 6% missing']`. Then simulate a lost page: 80 rows gives `['80 rows instead of 100']`.

### If your output differs

1. **`ModuleNotFoundError: No module named 'checks'`**: run from the repository folder, so that `chapters/ch20/examples` is found.
2. **`[]` twice**: the second scrape still uses `p.price`.

---

## Exercise 20.4 (harder)

> Write a log of a crawl of pages 1 to 3 of the library plus `/trouble/flaky` (after a reset) into `output/ch20/crawl.log`, with `PoliteClient` and a file handler. Then read the log file and print only the warning lines, without their time stamp. Expected output:

**What the question asks.** Record a short crawl in a log file, with time stamps, then read the file back with code and keep only the warnings, without their time stamp.

**The plan.** Add a `FileHandler` to the root logger with a format that separates the parts with ` | `. Reset the flaky page, crawl four addresses with `PoliteClient`, close the handler. Read the file line by line, split each line into three, print the warnings.

```python
import logging
import sys
from pathlib import Path

sys.path.insert(0, ".")
from toolkit.polite import PoliteClient  # noqa: E402

Path("output/ch20").mkdir(parents=True, exist_ok=True)
handler = logging.FileHandler(
    "output/ch20/crawl.log", mode="w", encoding="utf-8"
)
handler.setFormatter(
    logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
)
root = logging.getLogger()
root.setLevel(logging.INFO)
root.addHandler(handler)

client = PoliteClient("LearningScraper/1.0", delay=0.2, base_wait=0.3)
client.session.get(
    "http://localhost:8000/trouble/flaky/reset", timeout=10
)
for path in [
    "/library/",
    "/library/page-2.html",
    "/library/page-3.html",
    "/trouble/flaky",
]:
    client.get("http://localhost:8000" + path)
    logging.info("done %s", path)
handler.close()

for line in open("output/ch20/crawl.log", encoding="utf-8"):
    time_stamp, level, message = line.rstrip("\n").split(" | ")
    if level == "WARNING":
        print(level, message)
```

Output:

```text
WARNING status 503 on http://localhost:8000/trouble/flaky, retry 1 in 0.3 s
WARNING status 503 on http://localhost:8000/trouble/flaky, retry 2 in 0.6 s
```

**Line by line.**

- `logging.FileHandler("output/ch20/crawl.log", mode="w", encoding="utf-8")` writes log records to that file, replacing it on each run.
- `logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")` formats each record as time, level and message, separated by ` | `.
- `root = logging.getLogger()` is the root logger; `PoliteClient`'s logger, `polite`, passes its records up to it, so the handler receives them.
- `client.session.get(".../trouble/flaky/reset")` resets the flaky page, which then fails twice before succeeding.
- `logging.info("done %s", path)` adds your own line after each page.
- `handler.close()` writes everything to disk before you read the file.
- `line.rstrip("\n").split(" | ")` gives exactly three parts; the `if` keeps the warnings.

**Reading the result.** Two warnings, both for `/trouble/flaky`: status 503, retried after 0.3 s, then after 0.6 s. The third try worked, so there is no error line.

**Checking.** Open `output/ch20/crawl.log`: six lines, four `INFO` (one per page) and two `WARNING`, each starting with a date and time.

**Mistakes this exercise provokes.**

- A message that itself contains ` | `: the line splits into four parts and the unpacking fails. Choose a separator your messages never use.
- Reading the file before `handler.close()`: the last lines may not be written yet.
- `mode="a"` (the default): each run adds to the old log, and you print the warnings of every run.

**The choice it makes.** The format uses ` | ` between the parts, so each line splits cleanly into three. Choose a log format you can read back with code: you will want to count errors per night.

### Another way to solve it

Read the whole log into pandas. The separator ` | ` contains `|`, which means *or* in a regular expression, so escape it:

```python
import pandas as pd

log = pd.read_csv("output/ch20/crawl.log", sep=r" \| ", engine="python",
                  names=["time", "level", "message"])
print(log["level"].value_counts().to_dict())
```

```text
{'INFO': 4, 'WARNING': 2}
```

With `sep=" | "` unescaped, pandas splits at every space and fails with `ParserError`.

### A variation to try

Count the warnings per address: extract the address from each warning message with `message.split(" on ")[1].split(",")[0]`, and count with `Counter`. On a long crawl, one address with many warnings is a page to look at.

### If your output differs

1. **No warnings**: the flaky page was not reset, so it answered at once; check the reset request.
2. **`ValueError: too many values to unpack`**: a line has more than two ` | `; print it.
3. **Warnings from earlier runs**: use `mode="w"`.
