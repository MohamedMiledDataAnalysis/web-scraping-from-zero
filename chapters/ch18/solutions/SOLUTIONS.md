# Chapter 18 — detailed solutions

These are the long versions of the solutions printed in the book. Each has the same parts as the book, with more detail, plus parts the book has no room for: another way to solve the exercise, a variation to try, and what to do if your output differs.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 18.1 (easy)

> Try to log in with the right token but the password `wrong`. Print the status code and the error message. Expected output:

**What the question asks.** Send the login form with a valid security token but a wrong password, and see how the site refuses: the status code and the message it shows.

**The plan.** Same steps as a correct login: load the login page in a session, read the hidden `csrf_token`, post the form. Only the password changes. Then read the `p.error` paragraph of the answer.

```python
import requests
from bs4 import BeautifulSoup

BASE = "http://localhost:8000"
session = requests.Session()
page = BeautifulSoup(
    session.get(f"{BASE}/account/login", timeout=10).text, "html.parser"
)
token = page.select_one('input[name="csrf_token"]')["value"]
r = session.post(
    f"{BASE}/account/login",
    timeout=10,
    data={
        "csrf_token": token,
        "username": "reader",
        "password": "wrong",
    },
)
print(
    r.status_code,
    BeautifulSoup(r.text, "html.parser").select_one("p.error").text,
)
```

Output:

```text
400 Wrong username or password.
```

**Line by line.**

- `session.get(f"{BASE}/account/login")` loads the form; the session keeps the cookie that ties the token to you.
- `page.select_one('input[name="csrf_token"]')["value"]` reads the hidden token, a random value of 32 characters.
- `session.post(..., data={...})` sends the three fields the form contains: `csrf_token`, `username` and `password`.
- `r.status_code` is the answer's code; `select_one("p.error").text` is the message shown above the form.

**Reading the result.** `400 Wrong username or password.` The site refuses with *bad request* and a message that does not say which of the two was wrong, which is good security practice.

**Checking.** Post the same form **without** the token: status 400 too, but another message, `Security token missing or wrong. Load the login page first.` The two messages tell you which part of the request failed.

**Mistakes this exercise provokes.**

- Posting with `requests.post` instead of `session.post`: the token was issued to the session's cookie, so a request outside the session fails the token check, not the password check.
- Copying a token from your browser into the code: it belongs to the browser's session, not to your program's.
- Reading `p.error` on a successful login: there is none, and `.text` stops with `AttributeError`.

**The choice it makes.** The Practice Ground answers a failed login with status 400. Many real sites answer 200 with the same form: never rely on the status code alone; look for an element that only a logged-in user sees, as exercise 18.2 does.

### Another way to solve it

Collect the form's fields from the page instead of writing their names yourself, so that hidden fields are never forgotten:

```python
form = page.select_one("form")
data = {i["name"]: i.get("value", "") for i in form.select("input[name]")}
data.update({"username": "reader", "password": "wrong"})
r = session.post(f"{BASE}/account/login", data=data, timeout=10)
```

`data` starts as `{'csrf_token': '...', 'username': '', 'password': ''}`, then receives your values. On forms with several hidden fields, this saves you from missing one.

### A variation to try

Post without the token (`data` without `csrf_token`) and print the message: `Security token missing or wrong. Load the login page first.` Then post with a token from **another** session: the same message, because a token is valid only for the session that received it.

### If your output differs

1. **`AttributeError: 'NoneType' object has no attribute 'text'`**: the login succeeded (no error paragraph); check the password value.
2. **The token message instead of the password message**: the token was not sent, or not from the same session.

---

## Exercise 18.2 (medium)

> Write a function `login(session, username, password)` that returns `True` when the login worked (the page shows the user's name in `#user-name`) and `False` otherwise. Test it with the right and the wrong password, each in a new session. Expected output:

**What the question asks.** A function that logs in and reports success as `True` or `False`, judged by what the page shows, then two tests, each in a fresh session so that the first login does not help the second.

**The plan.** Inside `login`, do the token-and-post sequence of exercise 18.1. After the post, look for `#user-name`, the element only a logged-in user sees, and check that it holds the expected name.

```python
import requests
from bs4 import BeautifulSoup

BASE = "http://localhost:8000"


def login(session, username, password):
    page = BeautifulSoup(
        session.get(f"{BASE}/account/login", timeout=10).text,
        "html.parser",
    )
    token = page.select_one('input[name="csrf_token"]')["value"]
    r = session.post(
        f"{BASE}/account/login",
        timeout=10,
        data={
            "csrf_token": token,
            "username": username,
            "password": password,
        },
    )
    name = BeautifulSoup(r.text, "html.parser").select_one("#user-name")
    return name is not None and name.text == username


print(login(requests.Session(), "reader", "practice"))
print(login(requests.Session(), "reader", "wrong"))
```

Output:

```text
True
False
```

**Line by line.**

- `login(session, username, password)` receives the session, so the caller keeps it, logged in, for the next requests.
- The token is read fresh on each call: a token is valid for one session.
- After the post, `requests` follows the site's redirect to `/account/`, so `r.text` is the account page when the login worked, and the form again when it failed.
- `name is not None and name.text == username` is `True` only if the element exists **and** shows the right name. `and` stops at the first `False`, so `.text` is never read on `None`.

**Reading the result.** `True` with the right password, `False` with the wrong one. Each line comes from its own new session.

**Checking.** After a successful login, `session.cookies.keys()` shows one cookie, `session`. `r.history` holds one answer with status 302: the redirect from the form to `/account/`.

**Mistakes this exercise provokes.**

- Judging success by `r.status_code == 200`: here a failure gives 400, but on many sites both outcomes give 200.
- Reusing one session for both tests: here the second call still returns `False`, because the Practice Ground checks the password again. But on a site that skips the form for a logged-in visitor, the second test would prove nothing. A fresh session makes each test independent.
- Returning `name.text == username` without the `None` test: `AttributeError` on every failure.

**The choice it makes.** The check uses an element only a logged-in user sees, and also verifies the name in it. That is the most reliable sign of success, whatever status codes the site chooses.

### Another way to solve it

Judge success by where the site sends you: after a successful login, the final address is `/account/`; after a failure, you stay on the login page.

```python
return r.url.rstrip("/").endswith("/account")
```

It also returns `True` and `False`. Addresses change less often than page layouts, but some sites redirect even on failure; the page-content test is the safer default.

### A variation to try

Add a `logout(session)` function that requests `/account/logout`, then check with `login`'s test: after logging out, `/account/` no longer shows `#user-name`. A long-running scraper should log out when it finishes.

### If your output differs

1. **`True` twice**: the password is the same in both calls, or the site kept you logged in; use a new session for each test.
2. **`False` twice**: the token or the field names are wrong; print the form's inputs with `[i["name"] for i in page.select("form input")]`.

---

## Exercise 18.3 (medium)

> Log in with `requests`, download `orders.csv` into `output/ch18/orders.csv`, read it with pandas, and print the total of all orders and the orders still *On its way*. Expected output:

**What the question asks.** Log in, download a CSV file that only logged-in users can get, save it, read it with pandas, and answer two questions: the total of all orders, and which orders are still on their way.

**The plan.** The login sequence of exercise 18.1 with the right password; `session.get` the file; check the status; write the raw bytes to disk; `read_csv`; sum one column and filter on another.

```python
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE = "http://localhost:8000"
session = requests.Session()
page = BeautifulSoup(
    session.get(f"{BASE}/account/login", timeout=10).text, "html.parser"
)
session.post(
    f"{BASE}/account/login",
    timeout=10,
    data={
        "csrf_token": page.select_one('input[name="csrf_token"]')[
            "value"
        ],
        "username": "reader",
        "password": "practice",
    },
)
r = session.get(f"{BASE}/account/orders.csv", timeout=10)
r.raise_for_status()
path = Path("output/ch18/orders.csv")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_bytes(r.content)
orders = pd.read_csv(path)
print(f"Total: £{orders['total'].sum():.2f}")
print(
    orders.loc[
        orders["status"] == "On its way", ["number", "item"]
    ].to_string(index=False)
)
```

Output:

```text
Total: £344.32
  number                item
PG-20271 A River of Kingdoms
PG-20272   The Bright Meadow
```

**Line by line.**

- The `session.post` logs in; its result is not stored, because the cookie it sets lives in `session`.
- `session.get(f"{BASE}/account/orders.csv")` downloads the file with the login cookie.
- `r.raise_for_status()` stops on an error status.
- `path.parent.mkdir(parents=True, exist_ok=True)` creates `output/ch18`.
- `path.write_bytes(r.content)` saves the bytes exactly as received.
- `orders["total"].sum()` adds the totals; `:.2f` prints two decimals.
- `orders.loc[orders["status"] == "On its way", ["number", "item"]]` keeps the orders not yet delivered, with two columns.

**Reading the result.** £344.32 in total over 12 orders. Two orders, PG-20271 and PG-20272, are still on their way; the ten others are delivered.

**Checking.** `print(r.headers["Content-Type"])` shows `text/csv; charset=utf-8`. `orders["status"].value_counts()` gives 10 *Delivered* and 2 *On its way*.

**Mistakes this exercise provokes.**

- Without the login, `orders.csv` redirects to the login page, `requests` follows, and you save the login page's HTML under the name `orders.csv`; `read_csv` then fails or reads nonsense.
- `raise_for_status()` does not catch that case: the final page, the login form, has status 200.
- `path.write_text(r.text)`: works for this file, but changes line endings and encodings; `write_bytes(r.content)` keeps the file identical.

**The choice it makes.** When a site offers a download of your data, take it: it is cleaner than the table and it is the route the site meant for you. Check `r.headers["Content-Type"]` (here `text/csv`) before you save a download.

### Another way to solve it

Read the CSV from memory, without saving it, when you do not need the file:

```python
import io

orders = pd.read_csv(io.StringIO(r.text))
```

The same 12 orders. Save the file when you want a record of what you downloaded; read from memory for a one-off analysis.

### A variation to try

Total per status, and the average order:

```python
print(orders.groupby("status")["total"].sum().round(2))
print(round(orders["total"].mean(), 2))
```

Delivered orders total £296.87 and those on their way £47.45; the average order is £28.69.

### If your output differs

1. **`pandas.errors.ParserError`** or strange columns: the file is HTML, not CSV. Print `r.url`: it ends with `/account/login?next=/account/orders.csv` when the login failed.
2. **`KeyError: 'total'`**: same cause; print `orders.columns`.

---

## Exercise 18.4 (harder)

> Log in with Playwright, copy the browser's cookies into a `requests.Session`, close the browser, and use the session to print the number of orders on `/account/`. Expected output:

**What the question asks.** Log in with a real browser, then hand the login over to `requests`: copy the browser's cookies into a session, close the browser, and read the account page at `requests` speed.

**The plan.** Playwright fills the form and clicks *Log in*; when the address becomes `/account/`, read the context's cookies and close the browser. Set each cookie in a `requests.Session` and request `/account/`.

```python
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8000/account/login")
    page.get_by_label("Username").fill("reader")
    page.get_by_label("Password").fill("practice")
    page.get_by_role("button", name="Log in").click()
    page.wait_for_url("**/account/")
    cookies = context.cookies()
    browser.close()

session = requests.Session()
for c in cookies:
    session.cookies.set(c["name"], c["value"])
soup = BeautifulSoup(
    session.get("http://localhost:8000/account/", timeout=10).text,
    "html.parser",
)
print(
    len(soup.select("#orders tbody tr")),
    "orders, read without a browser",
)
```

Output:

```text
12 orders, read without a browser
```

**Line by line.**

- `browser.new_context()` creates an isolated browser profile; its cookies are the ones you will copy.
- `page.get_by_label("Username").fill("reader")` finds the input by its visible label and types into it, as a person would; the same for the password.
- `page.get_by_role("button", name="Log in").click()` clicks the button whose accessible name is *Log in*.
- `page.wait_for_url("**/account/")` waits until the browser has arrived on the account page: the login is done.
- `context.cookies()` returns a list of dictionaries, one per cookie, with `name`, `value`, `domain` and other fields.
- `session.cookies.set(c["name"], c["value"])` copies each cookie's name and value into the session.
- `soup.select("#orders tbody tr")` counts the rows of the orders table.

**Reading the result.** `12 orders, read without a browser`: the session is logged in, without ever posting the form itself.

**Checking.** Print `soup.select_one("#user-name").text`: `reader`. Remove the cookie loop and run again: 0 orders, because the account page redirects to the login form.

**Mistakes this exercise provokes.**

- Passing `domain=c["domain"]` copies the domain `localhost`, and `requests` refuses to send cookies for a domain without a dot: the session is not logged in and the program prints 0 orders. On real sites, whose domains contain a dot, passing the domain is correct and safer.
- Reading the cookies before `wait_for_url`: the login may not be finished, and the session cookie is missing.
- Reading `page.context.cookies()` after `browser.close()`: the browser is gone.

**The choice it makes.** The browser is used for 2 seconds, only to log in; everything else runs at `requests` speed. `cookies.set(name, value)` without a domain sends the cookie to every site the session visits: keep such a session for this one site.

### Another way to solve it

Read the orders table with pandas instead of counting rows:

```python
import io

import pandas as pd

html = session.get("http://localhost:8000/account/", timeout=10).text
orders = pd.read_html(io.StringIO(html), attrs={"id": "orders"})[0]
print(len(orders), "orders")
```

It prints `12 orders`, and `orders` now holds every column of the table.

### A variation to try

Save the cookies to a JSON file with `json.dump(cookies, f)` and load them in a second program, so that it starts logged in without opening a browser. Delete the file when you are done: it is a key to your account. Never commit such a file to Git.

### If your output differs

1. **`0 orders`**: the cookies were not sent; check that you did not pass `domain=`, and that `wait_for_url` succeeded.
2. **`TimeoutError` in `wait_for_url`**: the login failed in the browser; take a screenshot with `page.screenshot(path="login.png")` to see the page.
