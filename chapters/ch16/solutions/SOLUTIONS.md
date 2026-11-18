# Chapter 16 — detailed solutions

These are the long versions of the solutions printed in the book. Each has the same parts as the book, with more detail, plus parts the book has no room for: another way to solve the exercise, a variation to try, and what to do if your output differs.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 16.1 (easy)

> With Playwright, collect the texts of the quotes of `/quotes/js/` pages 1 to 4 by clicking *next* until there is none. Print the number of quotes and the last author. Expected output:

**What the question asks.** Read the JavaScript version of the quotes with a real browser, page after page, by clicking *next* until there is none, then report how many quotes and the last author.

**The plan.** Start Chromium with Playwright, open page 1, and loop: wait for the quotes, read their texts and authors, look for the *next* link; if there is none, stop; otherwise click it and wait for the new page.

```python
from playwright.sync_api import sync_playwright

texts, authors = [], []
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8000/quotes/js/")
    while True:
        page.wait_for_selector("div.quote")
        texts += page.locator("div.quote span.text").all_inner_texts()
        authors += page.locator("div.quote small.author").all_inner_texts()
        next_link = page.locator("li.next a")
        if next_link.count() == 0:
            break
        next_link.click()
        page.wait_for_load_state()
    browser.close()
print(len(texts), "quotes; last author:", authors[-1])
```

Output:

```text
40 quotes; last author: June Albright
```

**Line by line.**

- `with sync_playwright() as p:` starts Playwright and stops it cleanly at the end of the block.
- `p.chromium.launch()` starts a browser without a window; `browser.new_page()` opens a tab.
- `page.wait_for_selector("div.quote")` waits until the page's JavaScript has built the quotes.
- `page.locator("div.quote span.text").all_inner_texts()` returns the visible text of every match, as a list; `texts += ...` adds them.
- `next_link.count() == 0` checks, without waiting, whether the page has a *next* link.
- `next_link.click()` clicks it; `page.wait_for_load_state()` waits for the new page to finish loading.
- `browser.close()` closes the browser before the results are printed.

**Reading the result.** `40 quotes; last author: June Albright`: four pages of ten, the same 40 quotes as the HTML version of Chapter 12, read after JavaScript built them.

**Checking.** Print `page.url` at each turn of the loop: `/quotes/js/`, then `/quotes/js/page/2/` up to page 4. `len(set(texts))` is 40: no page read twice.

**Mistakes this exercise provokes.**

- `next_link.click()` without checking first: on page 4, Playwright waits 30 seconds for a link that will never come, then stops with `TimeoutError`.
- Reading the quotes right after `goto`, without waiting: on a slow machine the list can still be empty.
- Using `requests` and BeautifulSoup on `/quotes/js/`: the `div.quote` elements are not in the HTML, so you find none.

**The choice it makes.** `next_link.count() == 0` tests for the absence of *next* without waiting 30 seconds for it. `wait_for_load_state()` waits for the new page to load after the click; on sites where this is not enough, `page.wait_for_url(f"**/page/{n + 1}/")` (with `n` the current page) waits for the new address itself.

### Another way to solve it

No browser at all: the data of each page sits in its script, as exercise 11.4 showed.

```python
import json
import re

import requests

quotes = []
for n in range(1, 5):
    url = "http://localhost:8000/quotes/js/" + (f"page/{n}/" if n > 1 else "")
    html = requests.get(url, timeout=10).text
    quotes += json.loads(re.search(r"var data = (\[.*?\]);", html, re.DOTALL).group(1))
print(len(quotes), quotes[-1]["author"])
```

It prints `40 June Albright`, in a fraction of the time. Chapter 15's rule applies: when the data is reachable without a browser, skip the browser.

### A variation to try

Collect the quotes as dictionaries instead of two parallel lists: for each `div.quote`, read the text and the author inside it with `quote.locator("span.text").inner_text()`. Two lists that must stay in step are easy to break; one record per quote is safer.

### If your output differs

1. **`TimeoutError` after 30 seconds**: the loop clicks *next* on the last page; check the `count() == 0` test.
2. **`playwright._impl._errors.Error: Executable doesn't exist`**: run `playwright install chromium` (Chapter 0).
3. **20 or 30 quotes**: a page was read before it changed; add `page.wait_for_url(...)` after the click.

---

## Exercise 16.2 (medium)

> In the shop, choose the category *Kitchen* and the sort *Rating*, and print the three best products with their rating, as shown on the page. Expected output:

**What the question asks.** Use the shop's two menus (category *Kitchen*, sort *Rating*), then read the three best products from the page as it shows them.

**The plan.** Open the shop and wait for the first products. Choose both menus inside an `expect_response` block that waits for the API answer carrying **both** choices. Then wait for the status to say *of 30*, and read the first three cards.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8000/shop/")
    page.wait_for_selector("div.product")
    with page.expect_response(
        lambda r: "sort=rating" in r.url and "Kitchen" in r.url
    ):
        page.select_option("#category", "Kitchen")
        page.select_option("#sort", "rating")
    page.wait_for_function(
        "document.querySelector('#status').innerText.includes('of 30')"
    )
    cards = page.locator("div.product")
    for i in range(3):
        card = cards.nth(i)
        print(
            card.locator("p.rating").inner_text(),
            card.locator("h3").inner_text(),
        )
    browser.close()
```

Output:

```text
4.7 / 5 Pro Kettle
4.7 / 5 Classic Kettle
4.7 / 5 Compact Blender
```

**Line by line.**

- `page.select_option("#category", "Kitchen")` chooses a value in the menu with id `category`, exactly as a person would; the page's JavaScript then requests new products.
- `with page.expect_response(lambda r: ...)` waits, at the end of the block, for a network answer whose address matches the test: both `sort=rating` and `Kitchen`.
- `page.wait_for_function("...includes('of 30')")` waits until the status line reports the 30 Kitchen products.
- `cards.nth(i)` takes the card at position `i`; inside it, `p.rating` and `h3` give the rating and the name.

**Reading the result.** Three Kitchen products rated 4.7, *Pro Kettle* first. The rating is printed as the page writes it, `4.7 / 5`.

**Checking.** Ask the API directly: `/shop/api/products?category=Kitchen&sort=rating&per_page=4` returns the same three products at 4.7, then *Eco Scale* at 4.6.

**Mistakes this exercise provokes.**

- Reading the cards right after the second `select_option`: you may read the list of the first request (Kitchen, unsorted) or even the old list.
- `wait_for_selector("div.product")` after the menus: it is satisfied at once by the products already on the page.
- `cards[0]`: locators are not lists; use `cards.nth(0)` or `cards.first`.

**The choice it makes.** Choosing two menus sends two API requests. Waiting for the answer that has **both** `Kitchen` and `sort=rating` makes sure you read the final list, not the intermediate one.

### Another way to solve it

Skip the page and ask the API the same question:

```python
import requests

data = requests.get("http://localhost:8000/shop/api/products",
                    params={"category": "Kitchen", "sort": "rating", "per_page": 3}, timeout=10).json()
print([(p["rating"], p["name"]) for p in data["products"]])
```

```text
[(4.7, 'Pro Kettle'), (4.7, 'Classic Kettle'), (4.7, 'Compact Blender')]
```

The page version proves you can drive the menus; the API version is what you would use in production.

### A variation to try

Choose the category *Audio* and the sort *Price*, and print the cheapest three. Change the `expect_response` test to `"sort=price" in r.url and "Audio" in r.url`.

### If your output differs

1. **Products from another category**: the program read the page before the final answer; check the `expect_response` test.
2. **`TimeoutError` in `expect_response`**: the test never matched; print each response address with `page.on("response", lambda r: print(r.url))`.

---

## Exercise 16.3 (medium)

> Open a shop product page, `http://localhost:8000/shop/product/42`, wait for its name, and print the name, the price and the stock text. Expected output:

**What the question asks.** A single product page, built by JavaScript: wait for its name to appear, then read the name, the price and the stock text.

**The plan.** Open `/shop/product/42` and read three elements with locators. Locator methods wait for their element by themselves, so no separate wait is needed.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8000/shop/product/42")
    name = page.locator("h1.name").inner_text()
    price = page.locator("#product p.price").inner_text()
    stock = page.locator("#product p.stock").inner_text()
    print(name, price, stock)
    browser.close()
```

Output:

```text
Compact Notebook £124.17 In stock
```

**Line by line.**

- `page.goto(...)` opens the page; its JavaScript then requests `/shop/api/product/42` and fills `#product`.
- `page.locator("h1.name").inner_text()` waits until an `h1` with the class `name` exists (up to 30 seconds), then returns its visible text.
- `#product p.price` and `#product p.stock` read the price and the stock line inside the product block.

**Reading the result.** `Compact Notebook £124.17 In stock`: the values as the page displays them, with `£` and words.

**Checking.** `requests.get("http://localhost:8000/shop/api/product/42").json()` returns the same product: name *Compact Notebook*, price 124.17, `in_stock` `True`. Print `page.locator("#product").inner_text()` to see every line of the block.

**Mistakes this exercise provokes.**

- `page.content()` then BeautifulSoup, right after `goto`: the HTML may still be the empty shell, before JavaScript filled it.
- `page.inner_text("h1")`: works, but if the page had two `h1`, you would not know which one you read.
- A product that does not exist, such as 999: the site answers 404 with its *Page not found* page, and the locator waits 30 seconds for `#product`, then raises `TimeoutError`.

**The choice it makes.** No explicit wait: `inner_text()` on a locator waits for the element by itself. That is the main difference between Playwright locators and the `find` methods of BeautifulSoup, which look once and return `None`.

### Another way to solve it

Check the response status first, so that a missing product fails fast instead of after 30 seconds:

```python
response = page.goto("http://localhost:8000/shop/product/999")
if response.status != 200:
    print("No such product:", response.status)
```

For product 999 it prints `No such product: 404` at once. `page.goto` returns the response of the page itself.

### A variation to try

Read the rating line too, `#product p.rating`: `2.7 / 5 (474 reviews)`. Then extract the number of reviews with the regular expression of Chapter 13: `re.search(r"\((\d+) reviews\)", text).group(1)`.

### If your output differs

1. **`TimeoutError` waiting for `h1.name`**: the product does not exist, or the page structure differs; open the page in your browser.
2. **Empty strings**: you read the elements with `page.content()` before JavaScript ran.

---

## Exercise 16.4 (harder)

> Scroll the shop until all *Office* products are loaded (choose the category first), and print their number and their average price, read from the page. Expected output:

**What the question asks.** Load every *Office* product of the infinite-scroll shop by scrolling, then compute their number and average price from the page's text.

**The plan.** Choose the category; wait for the first answer; then scroll in a loop, each time waiting for **more** products than before, until the status line says *Showing 30*. Read all price texts and average them.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8000/shop/")
    page.wait_for_selector("div.product")
    page.select_option("#category", "Office")
    page.wait_for_function(
        "document.querySelector('#status').innerText.includes('of 30')"
    )
    for _ in range(20):  # never more than 20 scrolls
        if "Showing 30" in page.locator("#status").inner_text():
            break
        n = page.locator("div.product").count()
        page.mouse.wheel(0, 20000)
        page.wait_for_function(
            f"document.querySelectorAll('div.product').length > {n}",
            timeout=5000,
        )
    prices = page.locator("div.product p.price").all_inner_texts()
    browser.close()
values = [float(t.replace("£", "")) for t in prices]
print(
    len(values),
    "products, average £" + f"{sum(values) / len(values):.2f}",
)
```

Output:

```text
30 products, average £111.58
```

**Line by line.**

- `page.select_option("#category", "Office")` filters the shop; the status then reads `Showing 12 of 30 products`.
- `for _ in range(20):` limits the loop to 20 scrolls, whatever happens.
- `if "Showing 30" in ...: break` stops as soon as everything is loaded.
- `n = page.locator("div.product").count()` remembers how many products are on the page now.
- `page.mouse.wheel(0, 20000)` scrolls down by 20,000 pixels, which triggers the next batch.
- `page.wait_for_function(f"...length > {n}", timeout=5000)` waits until the page holds more than `n` products, for at most 5 seconds.
- After the loop, `all_inner_texts()` collects the 30 prices; `float(t.replace("£", ""))` converts each.

**Reading the result.** `30 products, average £111.58`. Three batches were loaded: 12, then 12 more, then the last 6.

**Checking.** Print the status after each scroll: *Showing 12 of 30*, *Showing 24 of 30*, *Showing 30 of 30*. Exercise 16.5 must give the same average from the API's numbers.

**Mistakes this exercise provokes.**

- `page.wait_for_timeout(2000)` after each scroll instead of waiting for more products: too short on a slow machine, wasted time on a fast one.
- `while True:` without a limit: if the site stops loading, the program runs for ever.
- Reading the prices before the last batch arrives: 24 products and a wrong average.

**The choice it makes.** Here the page itself says when everything is loaded (*Showing 30 of 30 products*): a clear stop condition. Between two scrolls, the program waits for **more** products than before, not for a fixed time. If no new products arrive within 5 seconds, `wait_for_function` raises `TimeoutError` and the script stops with a clear error; `range(20)` stops the loop if the status never says *Showing 30*.

### Another way to solve it

The hidden API of Chapter 15 gives the same 30 products in one request:

```python
import requests

data = requests.get("http://localhost:8000/shop/api/products",
                    params={"category": "Office", "per_page": 50}, timeout=10).json()
prices = [p["price"] for p in data["products"]]
print(len(prices), f"products, average £{sum(prices) / len(prices):.2f}")
```

It prints `30 products, average £111.58`. Scrolling is how a person gets the data; the API is how a program should, when it is available.

### A variation to try

Stop on the number of products instead of the status text: read the total from the status (`of 30`) with a regular expression once, then loop until `page.locator("div.product").count()` equals it. This works on sites whose status does not say *Showing*.

### If your output differs

1. **`24 products`**: the loop stopped one scroll too early; print the status at the end.
2. **`TimeoutError` in `wait_for_function`**: no new products arrived; open the shop in a browser and scroll by hand to see whether it loads.

---

## Exercise 16.5 (harder)

> Do exercise 16.4 again by catching the API answers instead of reading the page. Count the API answers you caught. Expected output:

**What the question asks.** The same Office products as exercise 16.4, but taken from the JSON answers the page receives while you scroll, instead of from its text; and how many such answers there were.

**The plan.** Before opening the page, register a listener with `page.on("response", ...)` that keeps every answer whose address contains `category=Office`. Then scroll exactly as in 16.4. At the end, flatten the batches and average the prices.

```python
from playwright.sync_api import sync_playwright

batches = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.on(
        "response",
        lambda r: (
            batches.append(r.json())
            if "category=Office" in r.url
            else None
        ),
    )
    page.goto("http://localhost:8000/shop/")
    page.wait_for_selector("div.product")
    page.select_option("#category", "Office")
    page.wait_for_function(
        "document.querySelector('#status').innerText.includes('of 30')"
    )
    for _ in range(20):
        if "Showing 30" in page.locator("#status").inner_text():
            break
        n = page.locator("div.product").count()
        page.mouse.wheel(0, 20000)
        page.wait_for_function(
            f"document.querySelectorAll('div.product').length > {n}",
            timeout=5000,
        )
    browser.close()
products = [p for b in batches for p in b["products"]]
prices = [p["price"] for p in products]
print(
    len(batches),
    "answers,",
    len(products),
    "products, average £" + f"{sum(prices) / len(prices):.2f}",
)
```

Output:

```text
3 answers, 30 products, average £111.58
```

**Line by line.**

- `page.on("response", function)` calls `function` for **every** response the page receives, from the moment it is registered.
- The `lambda` appends `r.json()` to `batches` when the address contains `category=Office`, and does nothing otherwise.
- The listener is registered **before** `page.goto` and the menu choice, so no answer is missed.
- The scrolling loop is the same as in 16.4: it makes the page request the next batches.
- `[p for b in batches for p in b["products"]]` flattens the list of batches into one list of products: read it as two nested `for` loops.
- `p["price"]` is already a number: no `£` to remove.

**Reading the result.** `3 answers, 30 products, average £111.58`: three batches of 12, 12 and 6, and the same average as exercise 16.4.

**Checking.** Print `[len(b["products"]) for b in batches]`: `[12, 12, 6]`. The ids of the 30 products are all different: `len({p["id"] for p in products})` is 30.

**Mistakes this exercise provokes.**

- Registering the listener after the menu choice: depending on timing, the first answer may already have passed, and you catch 2 answers and 18 products. A result that changes from run to run is the sign of a race.
- `"Office" in r.url` without `category=`: it would also catch an address that merely contains the word elsewhere.
- Calling `r.json()` on every response: images and the page itself are not JSON, and the listener raises errors.

**The choice it makes.** The same average as exercise 16.4, from clean JSON numbers instead of texts: the page and its data agree. Catching the answers is the bridge between Playwright and the hidden API: you let the browser make the requests, and read the data it receives.

### Another way to solve it

Wait for one specific answer with `expect_response`, instead of collecting all of them:

```python
with page.expect_response(lambda r: "category=Office" in r.url and "page=2" in r.url) as info:
    page.mouse.wheel(0, 20000)
print(info.value.url, len(info.value.json()["products"]))
```

```text
http://localhost:8000/shop/api/products?page=2&category=Office&sort=id 12
```

The address shows how the page asks for its data: `page`, `category` and `sort=id`, the default order. That is exactly the request you can then send with `requests`.

### A variation to try

Keep only the addresses, not the data: append `r.url` in the listener and print the three addresses. You have rediscovered the hidden API from the browser, as Chapter 15 does with the Network panel.

### If your output differs

1. **`2 answers, 18 products`**, sometimes: the listener was registered too late and lost the race with the first answer.
2. **`json.decoder.JSONDecodeError`** inside the listener: the filter is too loose and catches a non-JSON response.
