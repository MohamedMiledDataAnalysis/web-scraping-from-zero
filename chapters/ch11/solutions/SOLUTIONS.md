# Chapter 11 — detailed solutions

These are the long versions of the solutions printed in the book. Each has the same parts as the book, with more detail, plus parts the book has no room for: another way to solve the exercise, a variation to try, and what to do if your output differs.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 11.1 (easy)

> Write `parse_quote(div)` returning `text`, `author` and `tags` for one quote, and print the result for the first two quotes of page 2. Expected output:

**What the question asks.** A function that turns one quote block into a dictionary of three fields (text, author, tags), and that survives a block where a field is missing.

**The plan.** Inside the function, find each element once; return `None` for a missing text or author, and a list of tag texts, empty if there is none.

```python
import requests
from bs4 import BeautifulSoup


def parse_quote(div):
    text = div.select_one("span.text")
    author = div.select_one("small.author")
    return {
        "text": text.text.strip("“”") if text else None,
        "author": author.text if author else None,
        "tags": [a.text for a in div.select("a.tag")],
    }


html = requests.get(
    "http://localhost:8000/quotes/page/2/", timeout=10
).text
soup = BeautifulSoup(html, "html.parser")
for div in soup.select("div.quote")[:2]:
    print(parse_quote(div))
```

Output:

```text
{'text': 'Sawdust on the floor means something was made.', 'author': 'Walter Pike', 'tags': ['work', 'humour']}
{'text': 'Patience is not waiting; it is working while you wait.', 'author': 'Ada Fernhill', 'tags': ['patience', 'work']}
```

**Line by line.**

- `div.select_one("span.text")` returns the text element, or `None` if the block has none; the same for the author.
- `text.text.strip("“”") if text else None`: when the element exists, take its text and remove the curly quotation marks at both ends; otherwise `None`.
- `strip("“”")` removes **any** of the characters given, from both ends, not the two-character string: it handles each mark separately.
- `[a.text for a in div.select("a.tag")]` lists the tag texts; with no tag, the list is simply empty.
- In the test, `soup.select("div.quote")[:2]` keeps the first two blocks of page 2.

**Reading the result.** Two dictionaries. The first, by Walter Pike, has the tags `work` and `humour`; the text no longer starts with `“`. Each dictionary is one future row of a table.

**Checking.** Test the function on a block with no author and no tag, built by hand: `parse_quote(BeautifulSoup('<div class="quote"><span class="text">“Hi”</span></div>', "html.parser").div)` returns `{'text': 'Hi', 'author': None, 'tags': []}`, without crashing.

**Mistakes this exercise provokes.**

- `div.select_one("span.text").text` without the `if`: `AttributeError: 'NoneType' object has no attribute 'text'` on the first block without a text.
- `strip('"')` with straight quotes: the page uses curly quotes, `“` and `”`, so nothing is removed.
- Returning `None` for missing tags: every later step must then test for `None` before looping.

**The choice it makes.** A quote without tags gives an empty list, `[]`, not `None`: for a list field, empty is the natural *nothing*. For a single value (text, author), `None` says *absent*, which an empty string would hide.

### Another way to solve it

A small helper keeps the `if ... else None` in one place, which helps when a parser has many fields:

```python
def text_of(parent, selector):
    element = parent.select_one(selector)
    return element.text if element else None


def parse_quote(div):
    text = text_of(div, "span.text")
    return {
        "text": text.strip("“”") if text else None,
        "author": text_of(div, "small.author"),
        "tags": [a.text for a in div.select("a.tag")],
    }
```

Same results. Chapter 11's `parse_book_card` grows the same way.

### A variation to try

Parse all ten quotes of page 2 into a list, then print how many have the tag `work`: `sum("work" in q["tags"] for q in quotes)`. `True` counts as 1 when summed.

### If your output differs

1. **`AttributeError: 'NoneType' ...`**: a field has no `if` guard.
2. **Text still starting with `“`**: the characters in `strip` are straight quotes; copy the curly ones from the page or from the output of `repr()`.

---

## Exercise 11.2 (medium)

> Write `parse_job_item(li)` for the items of the job board (`li.job`): `id` (from `data-id`, as a number), `title`, `company`, `city`, `salary_min`, `salary_max` (numbers), `posted`, and `new` (`True` if the item has the *New* badge). Print the first job of the board. Expected output:

**What the question asks.** A parser for a job item with eight fields of four kinds: a number from an attribute, plain texts, two numbers cut from one salary text, a date from an attribute, and a yes-or-no that depends on whether an element exists.

**The plan.** One small helper, `money`, turns `£40,000` into 40000. The parser splits the salary text at its dash, reads `data-id` and `datetime`, and tests whether the *New* badge exists.

```python
import requests
from bs4 import BeautifulSoup


def money(text):
    return int(text.strip().replace("£", "").replace(",", ""))


def parse_job_item(li):
    low, high = li.select_one("p.salary").text.split("–")
    return {
        "id": int(li["data-id"]),
        "title": li.select_one("h2.job-title a").text,
        "company": li.select_one("p.company").text,
        "city": li.select_one("p.location").text,
        "salary_min": money(low),
        "salary_max": money(high),
        "posted": li.select_one("p.posted time")["datetime"],
        "new": li.select_one("span.badge") is not None,
    }


html = requests.get("http://localhost:8000/jobs/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
print(parse_job_item(soup.select_one("li.job")))
```

Output:

```text
{'id': 1252, 'title': 'Senior Credit Risk Analyst', 'company': 'Riverside Logistics', 'city': 'Leeds', 'salary_min': 75000, 'salary_max': 89000, 'posted': '2027-03-01', 'new': True}
```

**Line by line.**

- `money(text)` removes spaces, the `£` and the comma, then converts with `int`.
- `li.select_one("p.salary").text.split("–")` cuts `£75,000 – £89,000` at the en dash into `'£75,000 '` and `' £89,000'`; `low, high = ...` names the two pieces.
- `int(li["data-id"])` reads the attribute on the `li` itself and converts it.
- `li.select_one("p.posted time")["datetime"]` reads the date attribute, `2027-03-01`.
- `li.select_one("span.badge") is not None` is `True` when the badge exists and `False` otherwise: a boolean field.
- The test parses the first `li.job` of the board.

**Reading the result.** Job 1252, *Senior Credit Risk Analyst* at Riverside Logistics in Leeds, £75,000 to £89,000, posted on 1 March 2027, marked new. Numbers are numbers, the date is ISO text, and `new` is `True`.

**Checking.** Count the new jobs on page 1: `sum(parse_job_item(li)["new"] for li in soup.select("li.job"))` gives 8 of the 15 jobs.

**Mistakes this exercise provokes.**

- `split("-")` with a hyphen gives a list with one item, and `low, high = ...` stops with `ValueError: not enough values to unpack (expected 2, got 1)`.
- `"new": li.select_one("span.badge").text == "New"`: `AttributeError` on every job without a badge.
- `int(low)` without cleaning: `ValueError: invalid literal for int() with base 10: '£75,000 '`.

**The choice it makes.** The salary is written with an **en dash** (`–`), not a hyphen (`-`); copy the character from the page, or from the output of `repr()`. The date comes from the `datetime` attribute, a machine-readable ISO 8601 value whatever the visible text says.

### Another way to solve it

A regular expression finds the two amounts whatever the separator, as Chapter 13 shows:

```python
import re

amounts = re.findall(r"[\d,]+", li.select_one("p.salary").text)
salary_min, salary_max = (int(a.replace(",", "")) for a in amounts)
```

`re.findall` returns `['75,000', '89,000']`. This version keeps working if the site switches to a hyphen or to the word *to*.

### A variation to try

Parse every job of page 1 and print the titles of the new ones only:

```python
jobs = [parse_job_item(li) for li in soup.select("li.job")]
print([j["title"] for j in jobs if j["new"]])
```

### If your output differs

1. **`ValueError: not enough values to unpack`**: the dash in `split` is a hyphen; copy the en dash.
2. **`KeyError: 'datetime'`**: you selected `p.posted` instead of the `time` inside it.
3. **`new` always `False`**: check the badge's class with `print(li)`.

---

## Exercise 11.3 (medium)

> Print, from its JSON-LD, the name, price and availability (*InStock* or *OutOfStock*) of the books with ids 1 to 5. Their addresses are in the cards of page 1. Expected output:

**What the question asks.** Visit five detail pages and read three values from each page's JSON-LD block: the name, the price and the availability, shortened to `InStock` or `OutOfStock`.

**The plan.** Take the first five cards of page 1, build each detail address with `urljoin`, download the detail page, parse its JSON-LD with `json.loads`, and read the fields.

```python
import json
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

session = requests.Session()
base = "http://localhost:8000/library/"
soup = BeautifulSoup(session.get(base, timeout=10).text, "html.parser")
for card in soup.select("article.book-card")[:5]:
    url = urljoin(base, card.select_one("h3 a")["href"])
    page = BeautifulSoup(session.get(url, timeout=10).text, "html.parser")
    ld = json.loads(page.find("script", type="application/ld+json").string)
    status = ld["offers"]["availability"].rsplit("/", 1)[-1]
    print(ld["name"], ld["offers"]["price"], status)
```

Output:

```text
The Broken Forest 26.93 InStock
Salt Kingdom 19.20 InStock
A River of Maps 6.56 InStock
A Clockmaker of Mirrors 59.27 InStock
Beyond the Distant Kitchen 18.87 InStock
```

**Line by line.**

- `session = requests.Session()` reuses one connection for the six requests.
- `urljoin(base, card.select_one("h3 a")["href"])` turns `book/the-broken-forest-1.html` into a full address.
- `page.find("script", type="application/ld+json").string` is the JSON text inside the script tag.
- `json.loads(...)` turns it into a Python dictionary, `ld`.
- `ld["offers"]["price"]` goes into the nested dictionary `offers` and reads its `price`.
- `ld["offers"]["availability"]` is `https://schema.org/InStock`; `.rsplit("/", 1)[-1]` cuts at the **last** slash and keeps what follows: `InStock`.

**Reading the result.** Five books, all in stock, with prices from 6.56 to 59.27. The price comes as text, `"26.93"`, exactly as the JSON-LD writes it.

**Checking.** Compare with the cards on page 1: the same names and prices. `print(ld)` shows every field the block offers: author, genre, pages, year, rating.

**Mistakes this exercise provokes.**

- `ld["price"]`: `KeyError`, because the price is inside `offers`. Print `ld` and follow the nesting.
- `split("/")[1]` instead of `rsplit("/", 1)[-1]`: the second piece of `https://schema.org/InStock` is an empty string, because of the double slash.
- Treating the price as a number: `type(ld["offers"]["price"])` is `str`; convert with `float` before calculating.

**The choice it makes.** This is your first scraper that visits detail pages. Six requests are fine; for 1,000 books, Chapter 12 adds the delay and the checks that make it polite.

### Another way to solve it

The availability can also be shortened with `removeprefix`, which states exactly what is removed:

```python
status = ld["offers"]["availability"].removeprefix("https://schema.org/")
```

It gives `InStock` too, and leaves the value unchanged if a site ever writes it without the prefix.

### A variation to try

Print the JSON-LD `offers` block of one book in full with `json.dumps(ld["offers"])`:

```text
{"@type": "Offer", "price": "26.93", "priceCurrency": "GBP", "availability": "https://schema.org/InStock"}
```

The currency is there too, which the visible price only shows as `£`.

### If your output differs

1. **`AttributeError: 'NoneType' object has no attribute 'string'`**: the detail page has no JSON-LD block; print the address you requested.
2. **`json.decoder.JSONDecodeError`**: you passed the tag instead of its `.string`.

---

## Exercise 11.4 (medium)

> From the data inside the script of `/quotes/js/page/2/`, print the number of quotes and the list of distinct authors, sorted. Expected output:

**What the question asks.** Read the data that a page's JavaScript uses to build its quotes, straight from the HTML, without running the JavaScript: how many quotes, and which authors.

**The plan.** The script contains `var data = [ ... ];`. A regular expression captures the part between the brackets; `json.loads` turns it into a list of dictionaries.

```python
import json
import re

import requests

html = requests.get(
    "http://localhost:8000/quotes/js/page/2/", timeout=10
).text
match = re.search(r"var data = (\[.*?\]);", html, re.DOTALL)
quotes = json.loads(match.group(1))
print(len(quotes))
print(sorted({q["author"] for q in quotes}))
```

Output:

```text
10
['Ada Fernhill', 'Celeste Moreau', 'Henrik Sall', 'June Albright', 'Mira Okonkwo', 'Rashid Noor', 'Walter Pike']
```

**Line by line.**

- `requests.get(...).text` downloads the page's HTML, script included.
- `re.search(r"var data = (\[.*?\]);", html, re.DOTALL)` looks for `var data = `, then captures a `[`, as few characters as possible (`.*?`), and a `]` followed by `;`.
- `re.DOTALL` lets `.` match line breaks too, since the list may span several lines.
- `match.group(1)` is the captured text, the JSON list.
- `json.loads(...)` turns it into Python: a list of ten dictionaries with the keys `id`, `author`, `text` and `tags`.
- `{q["author"] for q in quotes}` is a *set comprehension*: it keeps each author once; `sorted` returns them in alphabetical order.

**Reading the result.** Ten quotes, by seven different authors. The set removes the repeats: Walter Pike and Rashid Noor each wrote two.

**Checking.** Open `/quotes/js/page/2/` in the browser: ten quotes appear, built from this data. `print(quotes[0])` shows the first one complete, the same as the first visible quote.

**Mistakes this exercise provokes.**

- `.*` instead of `.*?`: greedy, it runs to the **last** `];` of the page. Here there is only one, so it works, but on a page with several scripts it captures too much and `json.loads` fails.
- Forgetting `re.DOTALL` when the data spans several lines: `match` is `None`, and `.group(1)` stops with `AttributeError`.
- Parsing the page with BeautifulSoup and selecting `div.quote`: nothing, because those blocks only exist after the JavaScript runs.

**The choice it makes.** No BeautifulSoup at all: when you know the pattern, you can search the raw HTML directly. The pattern depends on the variable's name, `data`; if the site renames it, the scraper breaks, which is the cost of reading code instead of a documented format.

### Another way to solve it

Find the script with BeautifulSoup first, then apply the regular expression to its text only:

```python
soup = BeautifulSoup(html, "html.parser")
script = next(s.string for s in soup.find_all("script") if s.string and "var data" in s.string)
quotes = json.loads(re.search(r"var data = (\[.*?\]);", script, re.DOTALL).group(1))
```

Searching a smaller text reduces the chance of matching something elsewhere on the page.

### A variation to try

Which authors wrote more than one quote on page 2? `Counter(q["author"] for q in quotes).most_common(2)` gives `[('Walter Pike', 2), ('Rashid Noor', 2)]`.

### If your output differs

1. **`AttributeError: 'NoneType' object has no attribute 'group'`**: the pattern did not match; print the part of `html` around `var data` and compare the spaces.
2. **`json.decoder.JSONDecodeError`**: the capture includes too much or too little; print `match.group(1)[-50:]`.

---

## Exercise 11.5 (harder)

> Check that the visible price and the JSON-LD price of every book of page 1 are equal. Print the number of books checked and the number of differences. Expected output:

**What the question asks.** A consistency check across two sources of the same price: the visible price on each card of page 1, and the price in that book's JSON-LD. How many books were checked, and how many disagree?

**The plan.** For each card, read the visible price; visit the detail page and read the JSON-LD price; compare the two numbers with a small tolerance; count and report differences.

```python
import json
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

session = requests.Session()
base = "http://localhost:8000/library/"
soup = BeautifulSoup(session.get(base, timeout=10).text, "html.parser")
checked = differences = 0
for card in soup.select("article.book-card"):
    visible = float(card.select_one("p.price").text.replace("£", ""))
    url = urljoin(base, card.select_one("h3 a")["href"])
    page = BeautifulSoup(session.get(url, timeout=10).text, "html.parser")
    ld = json.loads(page.find("script", type="application/ld+json").string)
    checked += 1
    if abs(visible - float(ld["offers"]["price"])) > 0.001:
        differences += 1
        print("Difference:", url)
print(checked, "books checked,", differences, "differences")
```

Output:

```text
20 books checked, 0 differences
```

**Line by line.**

- `checked = differences = 0` starts two counters at 0 in one line.
- `float(card.select_one("p.price").text.replace("£", ""))` is the visible price as a number.
- `float(ld["offers"]["price"])` converts the JSON-LD price, which is text.
- `abs(visible - float(...)) > 0.001` is true when the two differ by more than a tenth of a penny.
- When they differ, the address is printed, so you can look at that page.
- The last line prints both counters.

**Reading the result.** `20 books checked, 0 differences`: the two sources agree on every book of page 1. A 0 is a meaningful result only because the counter of checked books is 20, not 0.

**Checking.** Make the test fail on purpose: add 1 to `visible` and run again. You get 20 `Difference:` lines and `20 differences`, which proves the comparison works.

**Mistakes this exercise provokes.**

- `visible == float(...)`: exact comparison of decimals can fail on rounding (`0.1 + 0.2 == 0.3` is `False` in Python).
- Comparing the texts, `"£26.93"` with `"26.93"`: always different.
- Printing only the differences, without the number checked: `0 differences` would look the same when nothing was checked at all.

**The choice it makes.** `abs(a - b) > 0.001` is the safe test for decimals. Cross-checking two sources of the same page is a good habit on real sites: a difference often reveals a promotion, a different currency, or a bug in your parser.

### Another way to solve it

Round both prices to pennies and compare: `round(visible, 2) != round(float(ld["offers"]["price"]), 2)`. For money with two decimals, rounding to 2 is equivalent to the tolerance test and reads more naturally.

### A variation to try

Extend the check to the availability: the card says *In stock* or *Out of stock*, and the JSON-LD says `InStock` or `OutOfStock`. Count the books where they disagree.

### If your output differs

1. **`20 differences`**: compare the two values for one book with `print(visible, ld["offers"]["price"])`; one of them is probably not cleaned.
2. **`0 books checked`**: the card selector found nothing.
