# Chapter 8 — detailed solutions

These are the long versions of the solutions printed in the book. Each has the same parts as the book, with more detail, plus parts the book has no room for: another way to solve the exercise, a variation to try, and what to do if your output differs.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 8.1 (easy)

> Use `params=` to search the job board for `python` in `London`, and print the address `requests` built and the number of results. Expected output:

**What the question asks.** Send a search to the job board the way its form would (keyword `python`, city `London`), let `requests` build the address, then print that address and the number of results.

**The plan.** Pass the two parameters as a dictionary to `params=`; read `r.url` to see the address; parse the page and read `.result-count`.

```python
import requests
from bs4 import BeautifulSoup

r = requests.get(
    "http://localhost:8000/jobs/",
    params={"q": "python", "city": "London"},
    timeout=10,
)
print(r.url)
print(
    BeautifulSoup(r.text, "html.parser")
    .select_one(".result-count")
    .text
)
```

Output:

```text
http://localhost:8000/jobs/?q=python&city=London
1 job
```

**Line by line.**

- `params={"q": "python", "city": "London"}` gives the parameters as a dictionary. `requests` adds `?q=python&city=London` to the address, with the `&` between them.
- `timeout=10` gives up if the site does not answer within 10 seconds.
- `r.url` is the final address `requests` actually requested, parameters included.
- The `print(...)` spreads a chain of calls over several lines inside brackets: parse the page, find `.result-count`, take its text.

**Reading the result.** The address ends with `?q=python&city=London`, exactly what the search form produces. One job matches: a single Python offer in London.

**Checking.** Paste the printed address into the browser: the page shows `1 job` and the offer *Senior Python Developer*. Remove the city, `params={"q": "python"}`: 12 jobs across all cities.

**Mistakes this exercise provokes.**

- Gluing the address yourself, `"...jobs/?q=" + keyword`: it works for `python`, but breaks for `data analyst`, whose space must be encoded. `params` encodes it as `data+analyst`.
- Writing the city in lower case: the Practice Ground matches cities exactly, so `london` finds 0 jobs. The keyword, on the other hand, ignores case: `Python` still finds 1.
- Reading `r.url` before the request: there is no `r` yet; `url` is known only once the request is sent.

**The choice it makes.** `params` builds correct addresses for any value, with spaces, accents or `&` inside. Glue text by hand only for fixed addresses.

### Another way to solve it

The same request with the address written by hand works for these two simple values:

```python
r = requests.get("http://localhost:8000/jobs/?q=python&city=London", timeout=10)
```

It gives `1 job` too. Try it with `q=data analyst` written by hand, then with `params`: `requests` turns the space into `+` and the address it prints is `http://localhost:8000/jobs/?q=data+analyst&city=London`.

### A variation to try

Print the titles of the matching jobs, not only their number:

```python
soup = BeautifulSoup(r.text, "html.parser")
print([a.text for a in soup.select("li.job h2 a")])
```

```text
['Senior Python Developer']
```

Then search for `python` in every city by removing `city` from `params`: 12 jobs.

### If your output differs

1. **`0 jobs`**: check the spelling and the capital letter of the city.
2. **An address with `%20`** instead of `+`: both encode a space; the site accepts either.
3. **`AttributeError: 'NoneType' object has no attribute 'text'`**: print `r.status_code` and `r.url`.

---

## Exercise 8.2 (easy)

> Request `/trouble/status/500`, `/trouble/status/200` and `/trouble/status/403` in a loop. For each, print `ok` or the error message of `raise_for_status()`. Expected output:

**What the question asks.** Three requests in a loop, one succeeding and two failing with different codes, and for each a clear line: `ok`, or the message `raise_for_status()` produces.

**The plan.** For each code, request the Trouble zone address that returns it; call `raise_for_status()` inside `try`; print `ok` if it passes, the error otherwise.

```python
import requests

for code in [500, 200, 403]:
    r = requests.get(
        f"http://localhost:8000/trouble/status/{code}", timeout=10
    )
    try:
        r.raise_for_status()
        print(code, "ok")
    except requests.HTTPError as error:
        print(code, error)
```

Output:

```text
500 500 Server Error: INTERNAL SERVER ERROR for url: http://localhost:8000/trouble/status/500
200 ok
403 403 Client Error: FORBIDDEN for url: http://localhost:8000/trouble/status/403
```

**Line by line.**

- `for code in [500, 200, 403]:` takes the three codes in turn.
- `f".../trouble/status/{code}"` builds the address that makes the Practice Ground answer with that code.
- `r.raise_for_status()` does nothing for codes below 400; for 400 and above it raises `requests.HTTPError`.
- The line after it, `print(code, "ok")`, runs only if no error was raised.
- `except requests.HTTPError as error:` catches that error and keeps it in `error`; `print(code, error)` prints its message.

**Reading the result.** `500 Server Error`, `200 ok`, `403 Client Error`. The message names the code, its reason (`INTERNAL SERVER ERROR`, `FORBIDDEN`) and the address. The loop goes on after each failure, because the error is caught inside it.

**Checking.** Add 404 and 429 to the list: `404 Client Error: NOT FOUND ...` and `429 Client Error: TOO MANY REQUESTS ...`. Print `r.ok` for each code: `True` only for 200.

**Mistakes this exercise provokes.**

- Putting the `try` around the whole loop: the first error (500) stops the loop, and 200 and 403 are never tried.
- `except Exception:` catches everything, including a typo inside the `try`, which then looks like a site error.
- Expecting `requests.get` itself to raise on 500: it does not; only `raise_for_status()` turns a bad code into an error.

**The choice it makes.** The message of an `HTTPError` says whether the error is on the client's side (4xx: your request) or the server's (5xx: the site). You will use that distinction in Chapter 20: retry 5xx, never retry 4xx except 429.

### Another way to solve it

Without exceptions, test the code yourself:

```python
for code in [500, 200, 403]:
    r = requests.get(f"http://localhost:8000/trouble/status/{code}", timeout=10)
    print(code, "ok" if r.ok else f"{r.status_code} {r.reason}")
```

It prints `500 500 INTERNAL SERVER ERROR`, `200 ok`, `403 403 FORBIDDEN`. Simpler for a loop like this one; `raise_for_status()` is better inside functions, where an error should travel up to the caller.

### A variation to try

Sort the codes into families: print `client error` for 400–499, `server error` for 500–599, and `ok` for the rest. `400 <= r.status_code < 500` tests the range in one expression.

### If your output differs

1. **The loop stops after 500**: the `try` is outside the loop.
2. **`ok` for every code**: `raise_for_status()` is missing.
3. **`ConnectionError`**: the Practice Ground is not running.

---

## Exercise 8.3 (medium)

> Download `eligible_assets.txt` from the Files section, and print its first line two ways: with `r.text` as `requests` decodes it, and with `r.content.decode("utf-16")`. Expected output:

**What the question asks.** See what happens when a site announces the wrong encoding, then read the same bytes correctly: the first line of a tab-separated file, decoded two ways.

**The plan.** Download the file; print the start of `r.text`, which `requests` decodes with the encoding the site announced; then decode the raw bytes, `r.content`, yourself as UTF-16, and print the first line.

```python
import requests

r = requests.get(
    "http://localhost:8000/files/eligible_assets.txt", timeout=10
)
print(repr(r.text[:30]))
print(repr(r.content.decode("utf-16").splitlines()[0]))
```

Output:

```text
'��I\x00S\x00I\x00N\x00\t\x00I\x00s\x00s\x00u\x00e\x00r\x00\t\x00A\x00s\x00'
'ISIN\tIssuer\tAsset type\tCurrency\tHaircut (%)\tMaturity'
```

**Line by line.**

- `r.text[:30]` is the first 30 characters of the text as `requests` decoded it, using the `charset` of the `Content-Type` header: here `utf-8`.
- `repr(...)` shows hidden characters, such as `\t` (tab) and `\x00` (a zero byte), instead of printing them invisibly.
- `r.content` is the raw bytes, not decoded.
- `.decode("utf-16")` turns the bytes into text using UTF-16; `.splitlines()[0]` keeps the first line.

**Reading the result.** The first line is garbage: `��` at the start, then a `\x00` between every letter. The second is a clean header: `ISIN`, `Issuer`, `Asset type`, `Currency`, `Haircut (%)`, `Maturity`, separated by tabs.

**Checking.** `print(r.headers["Content-Type"])` shows `text/plain; charset=utf-8`: the site claims UTF-8. `print(r.content[:2])` shows `b'\xff\xfe'`, the byte-order mark that starts a UTF-16 file. The file says one thing, the header another.

**Mistakes this exercise provokes.**

- Trusting `r.text` because no error appears: wrong decoding never raises an error, it produces wrong characters.
- `.decode("utf-8")` on the bytes: `UnicodeDecodeError`, because `\xff` is not valid UTF-8.
- Removing the `\x00` with `replace`: it hides the symptom and leaves the `��` and any accented character wrong.

**The choice it makes.** The site announces the file as UTF-8, which is wrong: it is UTF-16. UTF-16 stores each character on two bytes; read as a one-byte encoding, every second byte appears as `\x00`. If you see `\x00` everywhere, think UTF-16. Chapter 19 reads this file with pandas.

### Another way to solve it

Tell `requests` the right encoding, then use `r.text` as usual:

```python
r.encoding = "utf-16"
print(repr(r.text.splitlines()[0]))
print(len(r.text.splitlines()), "lines")
```

```text
'ISIN\tIssuer\tAsset type\tCurrency\tHaircut (%)\tMaturity'
41 lines
```

`r.apparent_encoding` guesses the encoding from the bytes themselves; here it returns `UTF-16`. Use it to find the right encoding, then set it explicitly: guesses can be wrong on short files.

### A variation to try

Read the file as a table with the `csv` module, giving it the tab as separator:

```python
import csv
import io

rows = list(csv.reader(io.StringIO(r.content.decode("utf-16")), delimiter="\t"))
print(rows[1][:3], len(rows) - 1, "assets")
```

```text
['PG79806111821', 'Issuer B SA', 'ABS'] 40 assets
```

### If your output differs

1. **`UnicodeDecodeError`**: you decoded with `utf-8`; use `utf-16`.
2. **A first line starting with `﻿`**: you decoded with `utf-16-le`, which keeps the byte-order mark as a character; `utf-16` removes it.

---

## Exercise 8.4 (harder)

> Write a function `fetch(session, url)` that returns the text of a page, or `None` after printing a short message when the request times out or the status is an error. Test it on `/library/`, `/trouble/slow?seconds=5` (with `timeout=2`) and `/trouble/status/404`. Expected output:

**What the question asks.** A small, reusable function that never crashes on the two problems you expect (a page too slow, an error status) and says what happened, then returns `None` so the caller can move on.

**The plan.** Inside `try`, request the page with a timeout and call `raise_for_status()`. Catch `requests.Timeout` and `requests.HTTPError` separately, each with its own message. Return the text when everything worked.

```python
import requests


def fetch(session, url, timeout=2):
    try:
        r = session.get(url, timeout=timeout)
        r.raise_for_status()
    except requests.Timeout:
        print("Timeout:", url)
        return None
    except requests.HTTPError as error:
        print("Error:", error)
        return None
    return r.text


session = requests.Session()
for path in [
    "/library/",
    "/trouble/slow?seconds=5",
    "/trouble/status/404",
]:
    html = fetch(session, "http://localhost:8000" + path)
    if html is not None:
        print("Got", len(html), "characters from", path)
```

Output:

```text
Got 9899 characters from /library/
Timeout: http://localhost:8000/trouble/slow?seconds=5
Error: 404 Client Error: NOT FOUND for url: http://localhost:8000/trouble/status/404
```

**Line by line.**

- `def fetch(session, url, timeout=2):` takes the session and the address; `timeout=2` is a default the caller can change.
- `session.get(url, timeout=timeout)` raises `requests.Timeout` if the site has not answered within 2 seconds.
- `r.raise_for_status()` raises `requests.HTTPError` for a code of 400 or more.
- Each `except` prints a message naming the problem and returns `None`.
- `return r.text` runs only when neither error happened.
- In the test loop, `if html is not None:` prints only the pages that came back.

**Reading the result.** The library page arrives (9,899 characters). The slow page, which takes 5 seconds, is abandoned after 2: `Timeout`. The missing page gives `Error: 404 Client Error`. The program reaches the end in about 2 seconds plus the library request.

**Checking.** Call `fetch(session, ".../trouble/slow?seconds=1")`: it arrives, because 1 second is under the limit. Raise the limit with `fetch(session, url, timeout=6)` and the 5-second page arrives too.

**Mistakes this exercise provokes.**

- `except Exception:` catches everything, including a typing mistake inside the function, and your scraper silently returns `None` for every page.
- No `timeout` at all: a slow or frozen site makes the program wait for ever.
- Catching `requests.ConnectionError` as well and returning `None`: if the whole site is down, every following request fails too, and the scraper keeps going for nothing.

**The choice it makes.** Two `except` blocks, one per error you expect, each with its own message. A `ConnectionError` (site down) is **not** caught: it should stop the program. Chapter 20 grows this function into `PoliteClient`, which also waits and retries.

### Another way to solve it

Return the error instead of printing it, so the caller decides what to do:

```python
def fetch(session, url, timeout=2):
    try:
        r = session.get(url, timeout=timeout)
        r.raise_for_status()
        return r.text, None
    except (requests.Timeout, requests.HTTPError) as error:
        return None, type(error).__name__
```

The caller writes `html, problem = fetch(session, url)` and can count timeouts and errors separately. A tuple in `except (A, B)` catches either error with one block.

### A variation to try

Record the failures: keep a list `failed = []`, and in the test loop append the path whenever `fetch` returns `None`. Print it at the end: `['/trouble/slow?seconds=5', '/trouble/status/404']`. A real scraper saves such a list and retries it later.

Note on exception types: the slow page raises `requests.ReadTimeout`, a kind of `requests.Timeout`, so `except requests.Timeout` catches it. A site that cannot be reached at all raises `requests.ConnectionError`, which is **not** a `Timeout`.

### If your output differs

1. **The program waits 5 seconds** on the slow page: the timeout is not passed to `session.get`.
2. **`ConnectionError`** stops the program: the Practice Ground is not running.
3. **A different number of characters** for `/library/`: your copy of the Practice Ground is older or newer than the book's; update the repository with `git pull`.
