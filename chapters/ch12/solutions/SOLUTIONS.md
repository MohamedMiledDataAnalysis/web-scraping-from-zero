# Chapter 12 — detailed solutions

These are the long versions of the solutions printed in the book. Each has the same parts as the book, with more detail, plus parts the book has no room for: another way to solve the exercise, a variation to try, and what to do if your output differs.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 12.1 (easy)

> Follow the *next* links of the quotes and print the number of pages and of quotes. Expected output:

**What the question asks.** Walk through every page of the quotes by following the *next* link until there is none, and report two totals: pages visited and quotes seen.

**The plan.** The pagination loop of section 12.2: start at page 1; on each page, count the quotes, find the *next* link, make it absolute; stop when there is no *next* link.

```python
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

session = requests.Session()
url, pages, quotes = "http://localhost:8000/quotes/", 0, 0
while url:
    soup = BeautifulSoup(session.get(url, timeout=10).text, "html.parser")
    pages += 1
    quotes += len(soup.select("div.quote"))
    nxt = soup.select_one("li.next a")
    url = urljoin(url, nxt["href"]) if nxt else None
    time.sleep(0.2)
print(pages, "pages,", quotes, "quotes")
```

Output:

```text
4 pages, 40 quotes
```

**Line by line.**

- `url, pages, quotes = "...", 0, 0` sets three variables in one line: the first address and two counters.
- `while url:` repeats as long as `url` is not `None`.
- `pages += 1` counts the page; `quotes += len(soup.select("div.quote"))` adds its quotes.
- `soup.select_one("li.next a")` finds the *next* link, or `None` on the last page.
- `urljoin(url, nxt["href"]) if nxt else None` builds the next address, or sets `url` to `None`, which ends the loop.
- `time.sleep(0.2)` waits between requests, as the site's terms ask.

**Reading the result.** `4 pages, 40 quotes`: ten quotes per page, four pages.

**Checking.** Open `/quotes/page/4/` in the browser: there is no *next* button. `/quotes/page/5/` answers 404.

**Mistakes this exercise provokes.**

- `url = nxt["href"]` without `urljoin`: `/quotes/page/2/` is not a full address, and `requests` stops with `MissingSchema`.
- Reading `nxt["href"]` without the `if nxt` test: `TypeError: 'NoneType' object is not subscriptable` on the last page.
- Forgetting the update of `url` inside the loop: the same page is read for ever.

**The choice it makes.** The quotes' *next* link is `/quotes/page/2/`, a link relative to the host; `urljoin` handles it like the library's `page-2.html`. One loop pattern, any kind of link: following the site's own links means you never guess how many pages there are.

### Another way to solve it

Count page numbers until a page has no quote:

```python
n, total = 1, 0
while True:
    r = session.get(f"http://localhost:8000/quotes/page/{n}/", timeout=10)
    found = len(BeautifulSoup(r.text, "html.parser").select("div.quote")) if r.ok else 0
    if not found:
        break
    total += found
    n += 1
print(n - 1, "pages,", total, "quotes")
```

It prints `4 pages, 40 quotes` too, after one extra request to page 5, which answers 404. This works when addresses follow a pattern; following *next* links works whatever the addresses look like, and costs no extra request.

### A variation to try

Print the address of each page as you visit it, and check that the last line printed is `/quotes/page/4/`. Then follow the *previous* links back from page 4 (`li.previous a`) to page 1.

### If your output differs

1. **`1 pages`**: the *next* selector found nothing; print `soup.select_one("li.next")`.
2. **The loop never ends**: `url` is not updated, or `urljoin` keeps returning the same address.

---

## Exercise 12.2 (medium)

> Collect every job of the job board on the site date (all pages; the *next* link is in `ul.pager li.next a`). Print the number of jobs and the three cities with the most jobs. Expected output:

**What the question asks.** Every job of the board on the site date, across all its pages, then the three cities with the most jobs.

**The plan.** The same pagination loop, with the board's own *next* selector, `ul.pager li.next a`; collect each job's city in a list; let `Counter` count them.

```python
import time
from collections import Counter
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

session = requests.Session()
url, cities = "http://localhost:8000/jobs/", []
while url:
    soup = BeautifulSoup(
        session.get(url, timeout=10).text, "html.parser"
    )
    cities += [
        li.select_one("p.location").text for li in soup.select("li.job")
    ]
    nxt = soup.select_one("ul.pager li.next a")
    url = urljoin(url, nxt["href"]) if nxt else None
    time.sleep(0.2)
print(len(cities), "jobs")
print(Counter(cities).most_common(3))
```

Output:

```text
50 jobs
[('Leeds', 12), ('Lyon', 10), ('Paris', 7)]
```

**Line by line.**

- `cities += [...]` adds the cities of the current page to the list.
- `ul.pager li.next a` is the *next* link inside the pager.
- `urljoin(url, nxt["href"])` handles a link that is only a query string, `?q=&city=&page=2`: it keeps the path `/jobs/` and replaces the query.
- `Counter(cities)` counts how many times each city appears; `.most_common(3)` returns the three largest counts with their cities.

**Reading the result.** 50 jobs, the same number the board announces at the top of page 1. Leeds leads with 12, then Lyon with 10 and Paris with 7.

**Checking.** `print(len(cities))` must equal the board's own count, `50 jobs`. Open the board with the city filter set to Leeds: 12 results.

**Mistakes this exercise provokes.**

- `li.next a` without `ul.pager`: correct on this page, but on a page with another list using the class `next`, it would pick the wrong link.
- Building page addresses yourself as `/jobs/page-2.html`: the board does not use that pattern; follow its links.
- `cities.append([...])` instead of `+=`: you get a list of lists, one per page, and `Counter` stops with `TypeError: unhashable type: 'list'`.

**The choice it makes.** `Counter` (from the standard module `collections`) counts the items of a list; `.most_common(3)` gives the three most frequent with their counts. For more columns, a DataFrame and `value_counts()` do the same, as below.

### Another way to solve it

Collect whole job records, then use pandas:

```python
import pandas as pd

# inside the loop:
rows += [{"city": li.select_one("p.location").text,
          "company": li.select_one("p.company").text}
         for li in soup.select("li.job")]
# after the loop:
df = pd.DataFrame(rows)
print(df["city"].value_counts().head(3).to_dict())
```

```text
{'Leeds': 12, 'Lyon': 10, 'Paris': 7}
```

With the records, other questions cost one line: `df["company"].nunique()` gives 9 companies, and `df["company"].value_counts().head(2)` shows Harbour Analytics with 10 offers.

### A variation to try

Collect the jobs of 15 March 2027 instead: start from `http://localhost:8000/jobs/?day=2027-03-15`. The *next* links keep the `day` parameter, so the loop stays on that date and collects 55 jobs, the count of exercise 6.1.

### If your output differs

1. **15 jobs**: only page 1 was read; the *next* selector found nothing.
2. **More than 50 jobs**: you started the site with `--live` or `--date`; restart it with `python run_site.py`.
3. **`TypeError: unhashable type: 'list'`**: use `+=`, not `append`.

---

## Exercise 12.3 (medium)

> For each tag of the quotes (the tag box), visit its page and count its quotes. Remember that a tag page can have several pages. Print the five most used tags. Expected output:

**What the question asks.** A count of quotes per tag, for the 16 tags of the tag box. Each tag has its own page, and a popular tag spreads over several pages; then the five most used tags.

**The plan.** Read the tag box once to get each tag's address. For each tag, run the pagination loop over its pages and add up the quotes. Sort the counts and print five.

```python
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

session = requests.Session()
base = "http://localhost:8000/quotes/"
home = BeautifulSoup(session.get(base, timeout=10).text, "html.parser")
tag_urls = {
    a.text: urljoin(base, a["href"])
    for a in home.select("aside.tag-box a")
}

counts = {}
for tag, url in tag_urls.items():
    n = 0
    while url:
        time.sleep(0.2)
        soup = BeautifulSoup(
            session.get(url, timeout=10).text, "html.parser"
        )
        n += len(soup.select("div.quote"))
        nxt = soup.select_one("li.next a")
        url = urljoin(url, nxt["href"]) if nxt else None
    counts[tag] = n

for tag, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[
    :5
]:
    print(tag, n)
```

Output:

```text
work 13
learning 9
habits 7
friendship 5
kindness 5
```

**Line by line.**

- `tag_urls = {a.text: urljoin(base, a["href"]) for a in ...}` maps each tag to the full address of its page.
- The outer `for` loop visits the tags; the inner `while` loop follows the pages of one tag.
- `n` counts that tag's quotes and is reset for each tag; `counts[tag] = n` stores the result.
- `sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))` sorts the pairs `(tag, count)`: first by count, largest first (the minus sign reverses the order of numbers), then by tag name.
- `[:5]` keeps the first five pairs.

**Reading the result.** `work` leads with 13 quotes, then `learning` (9) and `habits` (7). `friendship` and `kindness` tie at 5, and the alphabetical second key decides their order.

**Checking.** Open `/quotes/tag/work/`: it has a *next* button, and its second page holds the last 3 of the 13 quotes. Add up all 16 counts: more than 40, because one quote can have several tags.

**Mistakes this exercise provokes.**

- Counting only the first page of each tag gives at most 10 per tag: the *work* tag is undercounted at 10. Always check whether a list has more pages.
- Forgetting to reset `n = 0` for each tag: every count includes the tags before it.
- `sorted(..., reverse=True)` on the counts alone: ties come out in an order that depends on how the dictionary was filled.

**The choice it makes.** The sort key `(-kv[1], kv[0])` sorts by count, from the largest, then by name, so the order never depends on chance. The script makes 18 requests (the home page and 17 tag pages), all spaced by 0.2 seconds.

### Another way to solve it

Visit the four pages of quotes once and count the tags on the quotes themselves, with `Counter`:

```python
counts = Counter()
url = "http://localhost:8000/quotes/"
while url:
    soup = BeautifulSoup(session.get(url, timeout=10).text, "html.parser")
    counts.update(a.text for a in soup.select("div.quote a.tag"))
    nxt = soup.select_one("li.next a")
    url = urljoin(url, nxt["href"]) if nxt else None
print(counts.most_common(5))
```

```text
[('work', 13), ('learning', 9), ('habits', 7), ('questions', 5), ('friendship', 5)]
```

Four requests instead of eighteen, and the same counts. But look at the last two: `questions` and `friendship` tie at 5 with `kindness`, and `most_common` breaks the tie by the order it met the tags, not alphabetically. That is why the book's version sorts with an explicit second key.

### A variation to try

Print the tags that have only one quote: `[t for t, n in counts.items() if n == 1]`. Then print how many tags have more than one page of quotes: only `work`.

### If your output differs

1. **`work 10`**: the inner loop does not follow the tag's *next* link.
2. **The fifth line differs** (`questions` instead of `kindness`): ties are broken differently; add the name as a second sort key.

---

## Exercise 12.4 (harder)

> Visit the detail page of every book of the *Poetry* category and print the title of the book with the most pages, and the average rating of the category to two decimals. Reuse `book_parser.py`. Expected output:

**What the question asks.** A small crawler: walk the pages of the *Poetry* category, visit the detail page of each book, parse it with the parser of section 12.4, then answer two questions: which book has the most pages, and what is the category's average rating?

**The plan.** Import `parse_book_page` from the examples folder. Loop over the category's pages; for each card, build the detail address, download it, parse it, keep the record. Then `max` with a key, and an average.

```python
import sys
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, "chapters/ch12/examples")
from book_parser import parse_book_page  # noqa: E402

session = requests.Session()
url, records = "http://localhost:8000/library/category/poetry/", []
while url:
    soup = BeautifulSoup(
        session.get(url, timeout=10).text, "html.parser"
    )
    for a in soup.select("article.book-card h3 a"):
        detail = urljoin(url, a["href"])
        time.sleep(0.2)
        records.append(
            parse_book_page(
                detail, session.get(detail, timeout=10).text
            )
        )
    nxt = soup.select_one("li.next a")
    url = urljoin(url, nxt["href"]) if nxt else None

longest = max(records, key=lambda r: r["pages"])
print(longest["title"], longest["pages"])
print(round(sum(r["rating"] for r in records) / len(records), 2))
```

Output:

```text
Stations in the Map 693
3.27
```

**Line by line.**

- `sys.path.insert(0, "chapters/ch12/examples")` adds the examples folder to the places Python searches for imports; `from book_parser import parse_book_page` then finds the file. The comment `# noqa: E402` tells code checkers that an import after other code is intended.
- The outer `while` loop follows the category's *next* links; the inner `for` loop visits each book of the current page.
- `time.sleep(0.2)` before every detail request keeps the crawler polite.
- `parse_book_page(detail, html)` returns a dictionary with `title`, `pages`, `rating` and the other fields; `records.append(...)` keeps it.
- `max(records, key=lambda r: r["pages"])` returns the **record** with the largest `pages`, not just the number.
- `sum(r["rating"] for r in records) / len(records)` is the average rating; `round(..., 2)` keeps two decimals.

**Reading the result.** *Stations in the Map*, 693 pages, is the longest poetry book. The category's average rating is 3.27 stars out of 5.

**Checking.** `print(len(records))` gives the number of poetry books; compare it with the count the category page shows. Open the detail page of *Stations in the Map*: its information table shows 693 pages.

**Mistakes this exercise provokes.**

- Running the script from inside `chapters/ch12/solutions/`: the relative path in `sys.path.insert` no longer points to the examples, and the import fails with `ModuleNotFoundError: No module named 'book_parser'`. Run every program from the repository folder.
- `max(r["pages"] for r in records)`: you get 693 but not which book it is.
- Taking the rating from the card instead of the detail page: correct here, but the exercise practises the detail-page crawler of section 12.4.

**The choice it makes.** The solution lives in `solutions/`, and `book_parser.py` in `examples/`; `sys.path.insert` connects them. In a real project, you put shared code in one package; Chapter 21 shows how Scrapy organises it.

### Another way to solve it

Build a DataFrame from the records and let pandas answer both questions:

```python
import pandas as pd

books = pd.DataFrame(records)
print(books.loc[books["pages"].idxmax(), ["title", "pages"]].tolist())
print(round(books["rating"].mean(), 2))
```

It prints `['Stations in the Map', 693]` and `3.27`. With a DataFrame, further questions are one line each: `books.sort_values("pages").head(3)` for the three shortest.

### A variation to try

Run the same crawler on the *History* category (`/library/category/history/`), which has three pages. Then print the average price of the category, from the `price` field of the records.

### If your output differs

1. **`ModuleNotFoundError: No module named 'book_parser'`**: run the script from the repository folder.
2. **A different average**: one detail page failed to parse; print `len(records)` and compare it with the category's count.
