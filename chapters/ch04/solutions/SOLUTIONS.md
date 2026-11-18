# Chapter 4 — detailed solutions

These are the long versions of the solutions printed in the book. Each has the same parts as the book, with more detail, plus parts the book has no room for: another way to solve the exercise, a variation to try, and what to do if your output differs.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 4.1 (easy)

> Print the host, the path and the value of `q` in `http://localhost:8000/jobs/?q=python&city=London`. Expected output:

**What the question asks.** Split an address into its parts and print three of them: the host (`localhost`), the path (`/jobs/`) and the value of the parameter `q` (`python`).

**The plan.** `urlparse` cuts the address into named parts; `parse_qs` turns the query string (`q=python&city=London`) into a dictionary.

```python
from urllib.parse import urlparse, parse_qs

parts = urlparse("http://localhost:8000/jobs/?q=python&city=London")
print(parts.hostname)
print(parts.path)
print(parse_qs(parts.query)["q"][0])
```

Output:

```text
localhost
/jobs/
python
```

**Line by line.**

- `from urllib.parse import urlparse, parse_qs` loads two functions from Python's standard library: nothing to install.
- `urlparse(...)` returns an object whose attributes are the parts of the address: `scheme` (`http`), `netloc` (`localhost:8000`), `hostname`, `port`, `path`, `query`.
- `parts.hostname` is the host alone, without the port.
- `parts.path` is the part between the host and the `?`.
- `parts.query` is the text after the `?`: `q=python&city=London`.
- `parse_qs(parts.query)` turns it into `{'q': ['python'], 'city': ['London']}`; `["q"][0]` takes the first value of `q`.

**Reading the result.** Three lines: `localhost`, `/jobs/`, `python`. Each is plain text, ready to use in a program.

**Checking.** `print(parts)` shows every part at once. `print(parse_qs(parts.query))` shows the whole dictionary and explains why `[0]` is needed.

**Mistakes this exercise provokes.**

- `parts.netloc` gives `localhost:8000`, with the port; `hostname` gives the host alone.
- `parse_qs(parts.query)["q"]` without `[0]` prints `['python']`, a list: a name can appear several times in a query string (`q=a&q=b` gives `['a', 'b']`), so every value is a list.
- `parse_qs(...)["Q"]`: `KeyError: 'Q'`. Parameter names are case-sensitive.
- Splitting the address yourself with `split("?")` and `split("&")`: it works on this address and breaks on encoded characters such as `%20`.

**The choice it makes.** The standard library already parses addresses correctly, including the cases you have not met yet. Use it rather than cutting text by hand.

### Another way to solve it

`parse_qsl` returns pairs instead of lists, and `dict()` turns them into a simple dictionary:

```python
from urllib.parse import parse_qsl

params = dict(parse_qsl(parts.query))
print(params)
```

```text
{'q': 'python', 'city': 'London'}
```

Simpler to read, but if a name appears twice only the last value is kept. Use `parse_qs` when a parameter can repeat.

### A variation to try

Build a new address with other parameters: `urlencode` turns a dictionary into a query string, and `_replace` swaps one part of the parsed address:

```python
from urllib.parse import urlencode

new = parts._replace(query=urlencode({"q": "sql", "city": "Leeds"}))
print(new.geturl())
```

```text
http://localhost:8000/jobs/?q=sql&city=Leeds
```

Chapter 8 shows the shorter way when you request a page: `requests.get(url, params={...})`.

### If your output differs

1. **`localhost:8000`**: you printed `netloc`, not `hostname`.
2. **`['python']`**: add `[0]`.
3. **`KeyError`**: print `parse_qs(parts.query)` to see the exact names.

---

## Exercise 4.2 (easy)

> The last page of the History category has the address `http://localhost:8000/library/category/history/page-3.html`. Use `urljoin` to compute where these links lead from it: `page-2.html`, `../fiction/`, `/library/book/salt-kingdom-2.html`. Expected output:

**What the question asks.** Three links found on a page, in three forms (a file name, a path going up with `..`, a path starting with `/`), and the full address each one leads to.

**The plan.** `urljoin(base, link)` does what the browser does when you click: it combines the page's address with the link.

```python
from urllib.parse import urljoin

base = "http://localhost:8000/library/category/history/page-3.html"
for link in [
    "page-2.html",
    "../fiction/",
    "/library/book/salt-kingdom-2.html",
]:
    print(urljoin(base, link))
```

Output:

```text
http://localhost:8000/library/category/history/page-2.html
http://localhost:8000/library/category/fiction/
http://localhost:8000/library/book/salt-kingdom-2.html
```

**Line by line.**

- `base` is the address of the page that contains the links.
- The list holds the three links exactly as they would appear in `href` attributes.
- `urljoin(base, link)` returns the full address:
  - `page-2.html` has no `/`: it replaces the last part of the address, so it stays in the folder `.../history/`;
  - `../fiction/` starts with `..`: it goes up one folder, from `.../history/` to `.../category/`, then down into `fiction/`;
  - `/library/book/...` starts with `/`: it starts again from the host, whatever the current folder.

**Reading the result.** Three complete addresses, each starting with `http://localhost:8000/`. Paste them into the browser: each opens a real page.

**Checking.** Open the History category, page 3, in the browser, and hover over the *previous* link: the status bar shows the first address printed.

**Mistakes this exercise provokes.**

- Gluing text: `"http://localhost:8000" + "page-2.html"` gives `http://localhost:8000page-2.html`, and `base + link` gives `.../page-3.htmlpage-2.html`.
- A base without the final `/` or file name: `urljoin(".../category/history", "../fiction/")` gives `.../library/fiction/`, one folder too high, because `history` is then read as a file name, not a folder.
- Assuming every link is relative: an `href` can already be complete; `urljoin` leaves it unchanged, which is what you want.

**The choice it makes.** `urljoin` follows the same rules as the browser, so your scraper reaches the page a reader would reach by clicking. Chapter 12 uses it on every link it follows.

### Another way to solve it

For a link in the same folder, cutting the base at its last `/` gives the folder:

```python
folder = base.rsplit("/", 1)[0]
print(folder + "/page-2.html")
```

It prints the first address correctly, but this method fails for `../fiction/` and for `/library/...`. That is why `urljoin` exists: it handles every form.

### A variation to try

Predict, then check, the result of these three links from the same base:

- `https://example.com/x`: a complete address, returned unchanged;
- `?page=4`: only the query changes, `.../history/page-3.html?page=4`;
- `#top`: only the fragment is added, `.../history/page-3.html#top`; the browser stays on the same page.

### If your output differs

1. **One folder too high or too low**: print `base`; it must end with the file name or with `/`.
2. **`page-3.htmlpage-2.html`**: you used `+` instead of `urljoin`.

---

## Exercise 4.3 (medium)

> Request `http://localhost:8000/library/page-51.html` (the library has only 50 pages) and print the status code, whether the response is `ok`, and the text of its `h1`. Expected output:

**What the question asks.** Request a page that does not exist and observe what the server answers: the status code, whether `requests` considers it a success, and the page it sends anyway.

**The plan.** One request; print `status_code` and `ok`; parse the body and print its `h1`.

```python
import requests
from bs4 import BeautifulSoup

r = requests.get("http://localhost:8000/library/page-51.html")
print(r.status_code, r.ok)
soup = BeautifulSoup(r.text, "html.parser")
print(soup.h1.text)
```

Output:

```text
404 False
404 — Page not found
```

**Line by line.**

- `requests.get(...)` sends the request. It does **not** raise an error on a 404: it returns the answer, whatever its status.
- `r.status_code` is the three-digit code: 200 means found, 404 means not found.
- `r.ok` is `True` for codes below 400 and `False` otherwise.
- `BeautifulSoup(r.text, ...)` parses the body, which here is the site's error page.
- `soup.h1.text` is the text of the first `h1` of that page.

**Reading the result.** `404 False`, then `404 — Page not found`. The site sent a complete page with a title **and** an error code. A scraper that only looks at the content would see a normal page.

**Checking.** Open the same address in the browser: the same *Page not found* page appears. In the Network panel (Chapter 4), the request shows the status 404.

**Mistakes this exercise provokes.**

- Expecting an exception: `requests.get` returns normally on a 404, so a `try`/`except` around it catches nothing.
- Checking only `if soup.h1:`: the error page has an `h1` too.
- Reading the cards of the error page: there are none, and a loop over them silently prints nothing, the symptom of exercise 1.1's wrong address.

**The choice it makes.** Look at the code, not only at the content: an error page is a valid HTML page. From Chapter 8, `r.raise_for_status()` turns a bad code into an error that stops the program at the right place.

### Another way to solve it

`raise_for_status()` raises an `HTTPError` when the code is 400 or more, so the failure cannot go unnoticed:

```python
try:
    r.raise_for_status()
except requests.HTTPError as e:
    print("HTTPError", e)
```

```text
HTTPError 404 Client Error: NOT FOUND for url: http://localhost:8000/library/page-51.html
```

`r.reason` holds the words that go with the code, here `NOT FOUND`.

### A variation to try

Request three addresses and print each status: `/library/` (200), `/nothing` (404), and `/private/` (200). The last one exists: the Practice Ground answers it. Whether you may **scrape** it is another question, answered by `robots.txt` in Chapter 5, not by the status code.

### If your output differs

1. **`200 True`**: you requested an existing page; check the page number, 51.
2. **`AttributeError: 'NoneType' object has no attribute 'text'`**: the answer has no `h1`; print `r.text[:300]` to see what the server sent.
3. **`ConnectionError`**: the Practice Ground is not running.

---

## Exercise 4.4 (medium)

> Use the Elements panel on a book page of the library (click any title). Find the tag and the attributes of the script that contains `"@type": "Book"`. Then confirm it in Python: print the `type` attribute of every `script` tag of `http://localhost:8000/library/book/salt-kingdom-2.html`. Expected output:

**What the question asks.** Two ways of seeing the same thing. In the browser, find the `script` that holds `"@type": "Book"` and read its tag and attributes. In Python, list the `type` attribute of every `script` on the page.

**The plan.** In the Elements panel, search the page (Ctrl+F or Cmd+F) for `@type`; the panel highlights the `script` that contains it. Then, in Python, find every `script` tag and print its `type`.

```python
import requests
from bs4 import BeautifulSoup

url = "http://localhost:8000/library/book/salt-kingdom-2.html"
soup = BeautifulSoup(requests.get(url).text, "html.parser")
for script in soup.find_all("script"):
    print(script.get("type"))
```

Output:

```text
application/ld+json
```

**Line by line.**

- `requests.get(url).text` downloads the book page; `BeautifulSoup` parses it.
- `soup.find_all("script")` returns a list of every `<script>` element.
- `script.get("type")` returns the value of the `type` attribute, or `None` if the tag has none. `script["type"]` would stop with `KeyError` on a script without it.

**Reading the result.** One line, `application/ld+json`: the page has exactly one script, and its type is not JavaScript. It does not run any code; it describes the book in a standard format called JSON-LD, made for search engines.

**Checking.** In the Elements panel, the highlighted tag reads `<script type="application/ld+json">`, followed by a block starting `{"@context": "https://schema.org", "@type": "Book"`. Python and the browser agree.

**Mistakes this exercise provokes.**

- `script["type"]`: works here, but stops with `KeyError` on the many sites whose scripts have no `type`.
- Searching the page source (Ctrl+U) and the Elements panel interchangeably: here they agree; on pages built by JavaScript they do not (section 4.7).
- `soup.find("script")` instead of `find_all`: one script only, which happens to be enough on this page but not on most.

**The choice it makes.** JSON-LD is often the cleanest data on a page: named fields, written for machines. Before scraping visible text, check whether the page already offers it. Chapter 11 extracts it.

### Another way to solve it

Find the JSON-LD script directly by its type, and read its content with the `json` module:

```python
import json

block = soup.find("script", type="application/ld+json")
book = json.loads(block.string)
print(list(book)[:8])
print(book["name"])
```

```text
['@context', '@type', 'name', 'author', 'genre', 'numberOfPages', 'datePublished', 'aggregateRating']
Salt Kingdom
```

`block.string` is the text inside the tag; `json.loads` turns it into a Python dictionary. Chapter 11 does this for every book.

### A variation to try

Run the same loop on `http://localhost:8000/quotes/js/`. It prints `None`: that page has one script with no `type` attribute, which means ordinary JavaScript. That script builds the quotes in the browser, which is why Chapter 15 needs other methods for that page.

### If your output differs

1. **`KeyError: 'type'`**: use `script.get("type")`.
2. **Nothing printed**: the page has no script; check the address of the book.
