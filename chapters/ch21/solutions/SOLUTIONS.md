# Chapter 21 — detailed solutions

These are the long versions of the solutions printed in the book. Each has the same parts as the book, with more detail, plus parts the book has no room for: another way to solve the exercise, a variation to try, and what to do if your output differs.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 21.1 (easy)

> Change `quotes_spider.py` to collect the author pages instead: from each quote, follow the *(about)* link and yield the name, birth year and birthplace. Scrapy's duplicate filter visits each author once. Print the number of authors in the file. Expected output:

**What the question asks.** A spider with two kinds of pages: quote pages, where it finds author links and the *next* link, and author pages, where it extracts three fields. Then the number of authors in the exported file.

**The plan.** `parse` handles quote pages: it yields one request per *(about)* link, sent to `parse_author`, and one request for the next quote page, sent back to `parse`. `parse_author` yields one item per author. Scrapy runs the requests and exports the items.

```python
import json

import scrapy
from scrapy.crawler import CrawlerProcess


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    start_urls = ["http://localhost:8000/quotes/"]

    def parse(self, response):
        for href in response.css("span.by a::attr(href)").getall():
            yield response.follow(href, self.parse_author)
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        yield {
            "name": response.css("h1.author-title::text").get(),
            "born": response.css("span.author-born-date::text").get(),
            "place": response.css(
                "span.author-born-location::text"
            ).get(),
        }


process = CrawlerProcess(
    settings={
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 0.2,
        "LOG_LEVEL": "ERROR",
        "USER_AGENT": "LearningScraper/1.0 (+mailto:reader@example.com)",
        "FEEDS": {
            "output/ch21/authors.json": {
                "format": "json",
                "overwrite": True,
            }
        },
    }
)
process.crawl(AuthorsSpider)
process.start()
authors = json.load(open("output/ch21/authors.json", encoding="utf-8"))
print(len(authors), "authors")
```

Output:

```text
8 authors
```

**Line by line.**

- `response.css("span.by a::attr(href)").getall()` returns the addresses of the *(about)* links; `::attr(href)` is Scrapy's way to select an attribute in CSS.
- `response.follow(href, self.parse_author)` creates a request for that address, made complete automatically, whose answer goes to `parse_author`.
- `.get()` returns the first match or `None`, which ends the pagination on the last page.
- In `parse_author`, `::text` selects an element's text; each field comes from its own element.
- `FEEDS` tells Scrapy to write the items to `output/ch21/authors.json`, replacing the file.
- After `process.start()`, the program reads the file and counts its entries.

**Reading the result.** `8 authors`. The spider yields a request for each of the 40 *(about)* links on the four quote pages, but only 8 author pages are fetched.

**Checking.** Keep a handle on the crawler (`crawler = process.create_crawler(AuthorsSpider)`) and print its stats after the run: `dupefilter/filtered` is 32, the 40 links minus the 8 distinct authors, and `downloader/request_count` is 13 (`robots.txt`, four quote pages, eight author pages).

**Mistakes this exercise provokes.**

- `yield scrapy.Request(href, ...)` with the relative address: Scrapy refuses a URL without a scheme. `response.follow` makes it complete.
- `response.css("h1.author-title").get()` without `::text`: the whole element, tags included.
- Calling `process.start()` twice in one program: Scrapy's engine can start only once (exercise 21.4).

**The choice it makes.** Scrapy's **duplicate filter** drops a request for an address it has already scheduled: the visited set of Chapter 12 is built in. Sending a request through `dont_filter=True` turns the filter off for that request, which you need only for pages that change between visits.

### Another way to solve it

Collect the author addresses yourself and request each once, without relying on the duplicate filter:

```python
    def parse(self, response):
        for href in set(response.css("span.by a::attr(href)").getall()):
            yield response.follow(href, self.parse_author)
```

`set(...)` removes duplicates within one page only. Across pages, the same author still appears several times, and the filter still does the rest. Trust the filter; it is built for this.

### A variation to try

Add the author's description to the item, with `response.css(".author-description::text").get()`, and export to CSV instead of JSON: change the feed to `"output/ch21/authors.csv": {"format": "csv", "overwrite": True}`. Open the CSV in VS Code: the descriptions that contain commas are quoted, as in exercise 3.3.

### If your output differs

1. **`0 authors`** and an empty file: the selectors match nothing; test them in `scrapy shell http://localhost:8000/quotes/`.
2. **`ReactorNotRestartable`**: `process.start()` ran twice in the same program.
3. **More than 8 authors**: two addresses differ only by a final `/`; print them.

---

## Exercise 21.2 (medium)

> Write a spider that collects, for every category of the library, its name and the number of books announced on its first page, and exports it to `output/ch21/categories.csv`. Print the three largest categories. Expected output:

**What the question asks.** For each category of the library, its name and the number of books the category page announces, collected by a spider and exported to CSV; then the three largest categories.

**The plan.** `parse` reads the category links in the side menu and follows each, passing the link's text along with `cb_kwargs`. `parse_category` reads the number in `p.result-count strong` and yields one item. pandas reads the CSV and sorts.

```python
import pandas as pd
import scrapy
from scrapy.crawler import CrawlerProcess


class CategoriesSpider(scrapy.Spider):
    name = "categories"
    start_urls = ["http://localhost:8000/library/"]

    def parse(self, response):
        for a in response.css("aside.categories a"):
            yield response.follow(
                a,
                self.parse_category,
                cb_kwargs={"name": a.css("::text").get()},
            )

    def parse_category(self, response, name):
        count = response.css("p.result-count strong::text").get()
        yield {"category": name, "books": int(count)}


process = CrawlerProcess(
    settings={
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 0.2,
        "LOG_LEVEL": "ERROR",
        "USER_AGENT": "LearningScraper/1.0 (+mailto:reader@example.com)",
        "FEEDS": {
            "output/ch21/categories.csv": {
                "format": "csv",
                "overwrite": True,
            }
        },
    }
)
process.crawl(CategoriesSpider)
process.start()
cats = pd.read_csv("output/ch21/categories.csv")
print(
    cats.sort_values(["books", "category"], ascending=[False, True])
    .head(3)
    .to_string(index=False)
)
```

Output:

```text
category  books
  Travel     70
 Science     59
 Mystery     56
```

**Line by line.**

- `response.css("aside.categories a")` returns the 20 category links as selectors.
- `response.follow(a, self.parse_category, cb_kwargs={...})` follows the link and passes `name` to the callback as an extra argument.
- `a.css("::text").get()` is the link's text, the category's name.
- `def parse_category(self, response, name):` receives the response and the name.
- `p.result-count strong::text` is the first `strong` inside the count paragraph: the number of results, as text; `int(...)` converts it.
- `sort_values(["books", "category"], ascending=[False, True])` sorts by number of books, largest first, then by name for ties.

**Reading the result.** Travel is the largest category with 70 books, then Science (59) and Mystery (56).

**Checking.** Open `/library/category/travel/` in the browser: the count paragraph reads *70 results, page 1 of 4.* Add up the `books` column of the CSV: 1,000, every book in exactly one category.

**Mistakes this exercise provokes.**

- `p.result-count::text`: the text **outside** the `strong` tags, such as ` results, page `, not the number.
- Storing the name in `self.name` instead of passing it with `cb_kwargs`: `self.name` is the spider's own name, and requests finish in any order, so a shared variable would mix categories up.
- Sorting only by `books`: equal counts come out in an order that depends on which request finished first.

**The choice it makes.** `cb_kwargs` passes extra values to the callback: here the category's name, read on the page where you found the link. The count comes from the first page of each category, so the spider makes 21 requests instead of following every page.

### Another way to solve it

Read the name on the category page itself instead of passing it: if the page shows its category in the heading, `response.css("h1::text").get()` gives it, and `cb_kwargs` is no longer needed. Passing the value is safer when the target page does not repeat it, or writes it differently from the link.

### A variation to try

Yield the number of pages as well: the count paragraph's third `strong` holds it (`page 1 of 4`): `response.css("p.result-count strong::text").getall()[2]`. Then check that `books` divided by 20, rounded up, equals the number of pages for every category.

### If your output differs

1. **`ValueError: invalid literal for int()`**: the selector returned text other than the number; print `response.css("p.result-count").get()`.
2. **Fewer than 20 rows**: some requests failed; set `"LOG_LEVEL": "INFO"` to see why.

---

## Exercise 21.3 (medium)

> Add a pipeline to the jobs crawl that drops jobs whose maximum salary is under £50,000, and print how many jobs are kept. Expected output:

**What the question asks.** A pipeline that drops the jobs whose maximum salary is under £50,000, and a second one that counts what remains, on a crawl of the whole job board.

**The plan.** The spider yields the title and the maximum salary of each job and follows the pager. `HighSalaryPipeline` raises `DropItem` for low salaries; `CountPipeline`, which runs after it, counts the items that reach it and prints the count when the spider closes.

```python
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import DropItem


class JobsSpider(scrapy.Spider):
    name = "jobs"
    start_urls = ["http://localhost:8000/jobs/"]

    def parse(self, response):
        for li in response.css("li.job"):
            low, high = li.css("p.salary::text").get().split("–")
            yield {"title": li.css("h2.job-title a::text").get(),
                   "salary_max": int(high.strip(" £").replace(",", ""))}
        next_page = response.css("ul.pager li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)


class HighSalaryPipeline:
    def process_item(self, item):
        if item["salary_max"] < 50000:
            raise DropItem("salary too low")
        return item


class CountPipeline:
    def open_spider(self):
        self.count = 0

    def process_item(self, item):
        self.count += 1
        return item

    def close_spider(self):
        print(self.count, "jobs with a maximum salary of £50,000 or more")


process = CrawlerProcess(settings={
    "ROBOTSTXT_OBEY": True, "DOWNLOAD_DELAY": 0.2, "LOG_LEVEL": "ERROR",
    "USER_AGENT": "LearningScraper/1.0 (+mailto:reader@example.com)",
    "ITEM_PIPELINES": {"__main__.HighSalaryPipeline": 100,
                       "__main__.CountPipeline": 200}})
process.crawl(JobsSpider)
process.start()
```

Output:

```text
46 jobs with a maximum salary of £50,000 or more
```

**Line by line.**

- In the spider, `split("–")` cuts the salary text at the en dash; `high.strip(" £").replace(",", "")` removes the spaces, the `£` and the comma; `int` converts.
- `process_item(self, item)` receives every item. Returning the item passes it on; raising `DropItem` removes it, and later pipelines never see it.
- `open_spider(self)` runs once at the start: it sets the counter to 0. `close_spider(self)` runs once at the end: it prints the count.
- `ITEM_PIPELINES` lists the pipelines with a number: lower numbers run first, so the filter (100) runs before the counter (200).
- `"__main__.HighSalaryPipeline"` names the class by its module; a script run directly is the module `__main__`.

**Reading the result.** 46 of the 50 jobs have a maximum salary of £50,000 or more. Four were dropped.

**Checking.** Swap the numbers (filter 200, counter 100): the counter now runs first and prints 50, every job. Set `"LOG_LEVEL": "INFO"`: Scrapy reports four dropped items in its final stats.

**Mistakes this exercise provokes.**

- Pipeline methods with a `spider` parameter (`process_item(self, item, spider)`): the pinned Scrapy 2.20 warns that the argument is deprecated and will stop being passed. The book's signatures avoid it.
- Returning `None` instead of the item: the next pipeline receives nothing useful, and the export is empty.
- Filtering by `salary_max < 50000` with the text value: comparing text with a number raises `TypeError`.

**The choice it makes.** The counting pipeline comes **after** the filter (200 after 100), so it counts only the jobs that passed. Pipelines keep the spider about pages and the pipelines about data: cleaning, filtering and saving can change without touching the spider.

### Another way to solve it

Filter in the spider instead, by not yielding low salaries:

```python
            salary_max = int(high.strip(" £").replace(",", ""))
            if salary_max >= 50000:
                yield {"title": li.css("h2.job-title a::text").get(),
                       "salary_max": salary_max}
```

The same 46 jobs. Simpler for one rule; a pipeline is better when several spiders share the rule, or when you want the dropped count in the stats.

### A variation to try

Make the threshold a setting: in the pipeline, add `@classmethod def from_crawler(cls, crawler)` that reads `crawler.settings.getint("MIN_SALARY", 50000)` and stores it. Then run with `"MIN_SALARY": 70000` and compare the count.

### If your output differs

1. **`50 jobs`**: the filter runs after the counter; check the numbers in `ITEM_PIPELINES`.
2. **`ScrapyDeprecationWarning`** in the output: a pipeline method still has a `spider` parameter.
3. **`ValueError: not enough values to unpack`**: the dash in `split` is a hyphen; copy the en dash.

---

## Exercise 21.4 (harder)

> Run the library spider with `CLOSESPIDER_ITEMCOUNT` set to 30 and `HTTPCACHE_ENABLED` set to `True`, twice, and print the number of items each time and whether the second run sent requests to the site. Use the `httpcache/hit` statistic of the crawler's stats. Expected output:

**What the question asks.** See Scrapy's HTTP cache at work: two identical runs that stop after 30 items, the first fetching from the site and the second from the disk, proven by the `httpcache/hit` statistic.

**The plan.** Because `process.start()` can run only once per program, put the crawl in a small program (the text `code`) and run it twice in new Python processes with `subprocess.run`. Each run prints whether it got at least 30 items and whether any page came from the cache.

```python
import subprocess
import sys

code = r"""
import os
import sys
sys.path.insert(0, "chapters/ch21/examples")
from scrapy.crawler import CrawlerProcess
from library_spider import LibrarySpider
process = CrawlerProcess(settings={
    "CLOSESPIDER_ITEMCOUNT": 30, "HTTPCACHE_ENABLED": True,
    "HTTPCACHE_DIR": os.path.abspath("output/ch21/httpcache"),
    "LOG_LEVEL": "ERROR",
    "FEEDS": {"output/ch21/first30.json":
              {"format": "json", "overwrite": True}}})
crawler = process.create_crawler(LibrarySpider)
process.crawl(crawler)
process.start()
stats = crawler.stats.get_stats()
print(stats.get("item_scraped_count", 0) >= 30, "| from cache:",
      stats.get("httpcache/hit", 0) > 0)
"""
import shutil  # noqa: E402

shutil.rmtree("output/ch21/httpcache", ignore_errors=True)  # fresh start
for run in [1, 2]:
    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True
    )
    print("Run", run, "- at least 30 items:", result.stdout.strip())
```

Output:

```text
Run 1 - at least 30 items: True | from cache: False
Run 2 - at least 30 items: True | from cache: True
```

**Line by line.**

- `code = r"""..."""` holds a complete Python program as text.
- In it, `CLOSESPIDER_ITEMCOUNT: 30` stops the crawl after about 30 items; `HTTPCACHE_ENABLED: True` stores every response on disk and reuses it next time.
- `HTTPCACHE_DIR` is made absolute with `os.path.abspath`.
- `process.create_crawler(LibrarySpider)` keeps a handle on the crawler, so its statistics can be read after the run.
- `stats.get("httpcache/hit", 0) > 0` is `True` when at least one response came from the cache.
- `shutil.rmtree(..., ignore_errors=True)` deletes the cache before the first run, so the test starts clean.
- `subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)` runs the program in a new Python and captures what it prints.

**Reading the result.** Run 1: at least 30 items, nothing from the cache. Run 2: at least 30 items, from the cache. The second run did not ask the site for those pages.

**Checking.** Look inside `output/ch21/httpcache/`: one folder per spider, holding the stored responses. Run the solution a third time: the cache is deleted first, so run 1 again reports `False`.

**Mistakes this exercise provokes.**

- Calling `process.start()` twice in one program: `twisted.internet.error.ReactorNotRestartable`.
- A relative `HTTPCACHE_DIR`: Scrapy places it inside its hidden `.scrapy` folder, and you look for the cache in the wrong place.
- Expecting exactly 30 items: requests already in progress still finish, so the count can be a little higher.

**The choice it makes.** The cache makes repeated development runs free for the site: you can change your parsing code and run again without sending a single request. Delete it when you want fresh data; never ship a scraper that silently reads old pages.

### Another way to solve it

Instead of `subprocess`, run the two crawls from the command line, which also gives each run its own process:

```text
$ scrapy runspider chapters/ch21/examples/library_spider.py -s HTTPCACHE_ENABLED=True -s CLOSESPIDER_ITEMCOUNT=30 -O output/ch21/first30.json
```

Run it twice and compare the final statistics Scrapy prints: on the second run, `httpcache/hit` appears and `downloader/request_count` shows requests answered from the disk.

### A variation to try

Set `"HTTPCACHE_EXPIRATION_SECS": 60`: responses older than a minute are fetched again. Run twice within a minute (cache hits), then wait a minute and run again (no hits). This is how a scraper keeps a cache without serving stale data for ever.

### If your output differs

1. **`from cache: False` on run 2**: the cache folder was deleted between runs, or `HTTPCACHE_DIR` differs; print it.
2. **Empty output for a run**: the program in `code` raised an error; print `result.stderr`.
