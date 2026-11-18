# Chapter 15 — detailed solutions

These are the long versions of the solutions printed in the book. Each has the same parts as the book, with more detail, plus parts the book has no room for: another way to solve the exercise, a variation to try, and what to do if your output differs.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 15.1 (easy)

> With the hidden API, print the three highest-rated products of the *Office* category (use `sort=rating`). Expected output:

**What the question asks.** The three best-rated products of the *Office* category, using the shop's hidden API and its own sorting, rather than scraping the page.

**The plan.** One request to `/shop/api/products` with three parameters: the category, `sort=rating` (best first), and `per_page=3` so that the server returns only three products.

```python
import requests

data = requests.get(
    "http://localhost:8000/shop/api/products",
    params={"category": "Office", "sort": "rating", "per_page": 3},
    timeout=10,
).json()
for p in data["products"]:
    print(p["rating"], p["name"])
```

Output:

```text
4.9 Classic Notebook
4.9 Travel Chair Cushion
4.9 Smart Chair Cushion
```

**Line by line.**

- `params={"category": "Office", "sort": "rating", "per_page": 3}` gives the API the same choices the shop page's menus send.
- `.json()` returns a dictionary with `page`, `pages`, `total` and `products`.
- The loop prints each product's rating and name.

**Reading the result.** Three Office products rated 4.9. `total` in the answer is 30: the category holds 30 products, and you downloaded three.

**Checking.** Ask for five instead of three: a fourth product, *Mini Chair Cushion*, also has 4.9, and the fifth has 4.8. The API breaks the tie by product id (39, 57, 59, then 60), so *best three* here really means *three of the four best*.

**Mistakes this exercise provokes.**

- `category=office` in lower case: zero products and `total` 0, without an error. The API compares names exactly.
- Asking for all products and sorting in Python: correct, but you download 30 products to keep 3.
- Trusting a *top three* without looking at ties: when values are equal, the order depends on a rule you did not choose.

**The choice it makes.** Let the server sort and limit: you download three products instead of thirty. When ties matter, sort yourself with a second key, as below.

### Another way to solve it

Download the whole category and sort in pandas with an explicit tie-break, the name:

```python
import pandas as pd

data = requests.get("http://localhost:8000/shop/api/products",
                    params={"category": "Office", "per_page": 50}, timeout=10).json()
df = pd.DataFrame(data["products"])
top = df.sort_values(["rating", "name"], ascending=[False, True]).head(3)
print(top[["rating", "name"]].to_string(index=False))
```

```text
 rating                name
    4.9    Classic Notebook
    4.9  Mini Chair Cushion
    4.9 Smart Chair Cushion
```

A different third product: the tie is broken alphabetically, not by id. Both are correct; what matters is knowing which rule you used.

### A variation to try

Print the three cheapest Office products with `sort=price`. Then try `sort=-rating` and see what the API does with a value it does not document: it ignores it and returns the default order.

### If your output differs

1. **Nothing printed**: check the case of `Office`.
2. **Different products at 4.9**: the tie order changed; compare the ids.

---

## Exercise 15.2 (medium)

> Open a product page of the shop (click a name). Find, in the Network panel, the request that brings the product, and print with `requests` the name, price and reviews of products 7, 8 and 9. Expected output:

**What the question asks.** Find, in the browser's Network panel, the request a product page sends to get its data, then send that request yourself for three products.

**The plan.** Open `/shop/product/7` with the developer tools open, on the *Network* tab, filtered on *Fetch/XHR*. One request appears: `/shop/api/product/7`. Its address has the product id at the end, so loop over 7, 8 and 9.

```python
import requests

session = requests.Session()
for pid in [7, 8, 9]:
    p = session.get(
        f"http://localhost:8000/shop/api/product/{pid}", timeout=10
    ).json()
    print(pid, p["name"], p["price"], p["reviews"])
```

Output:

```text
7 Eco Toaster 117.15 518
8 Classic Toaster 90.52 771
9 Travel Toaster 78.58 406
```

**Line by line.**

- `session = requests.Session()` reuses the connection for the three requests.
- `f".../shop/api/product/{pid}"` builds the API address for each id.
- `.json()` returns one product as a dictionary with eight fields: `category`, `id`, `in_stock`, `name`, `price`, `rating`, `reviews`, `sku`.
- `print(pid, p["name"], p["price"], p["reviews"])` prints the three fields asked for.

**Reading the result.** Three toasters, from £78.58 to £117.15, with 406 to 771 reviews. The values are numbers in the JSON, ready to use.

**Checking.** Open `http://localhost:8000/shop/api/product/7` in the browser: it shows the same JSON. Then download the product **page**, `/shop/product/7`, with `requests` and search its text for `Eco Toaster`: it is not there, because the page's JavaScript fills in the name after loading.

**Mistakes this exercise provokes.**

- Requesting the page address, `/shop/product/7`, and parsing it with BeautifulSoup: the name and price are not in the HTML.
- Guessing the API address instead of reading it in the Network panel: `/shop/api/products/7` (with an *s*) does not exist.
- An id that does not exist: the API answers 404 with `{"error": "No product with this id"}`; `.json()["name"]` then stops with `KeyError`.

**The choice it makes.** The product page's address is `/shop/product/7`; the request its JavaScript sends is `/shop/api/product/7`. The page and the data have different addresses: always look in the Network panel, never guess.

### Another way to solve it

Check the status before reading the fields, so that a missing product is reported instead of crashing:

```python
for pid in [7, 8, 999]:
    r = session.get(f"http://localhost:8000/shop/api/product/{pid}", timeout=10)
    if r.ok:
        p = r.json()
        print(pid, p["name"], p["price"], p["reviews"])
    else:
        print(pid, r.status_code, r.json()["error"])
```

For 999 it prints `999 404 No product with this id`.

### A variation to try

Collect products 1 to 12 into a DataFrame and print the three with the most reviews. Wait 0.2 seconds between requests: 12 requests in a loop are still a burst.

### If your output differs

1. **`KeyError: 'name'`**: the API returned an error; print `r.status_code` and `r.text`.
2. **`json.decoder.JSONDecodeError`**: you requested the page, not the API.

---

## Exercise 15.3 (medium)

> Collect all 120 products with `per_page=50`, and print the number of requests, the number of products out of stock and the most reviewed product. Expected output:

**What the question asks.** All 120 products in as few requests as the API allows, then three facts: how many requests it took, how many products are out of stock, and which product has the most reviews.

**The plan.** Ask for 50 products per page, the API's maximum. Loop while the page number is not past the `pages` value the API returns. Build a DataFrame and answer with `~`, `sum` and `idxmax`.

```python
import time

import pandas as pd
import requests

session = requests.Session()
url = "http://localhost:8000/shop/api/products"
products, page, pages, calls = [], 1, 1, 0
while page <= pages:
    data = session.get(
        url, params={"page": page, "per_page": 50}, timeout=10
    ).json()
    calls += 1
    products += data["products"]
    pages = data["pages"]
    page += 1
    time.sleep(0.2)
df = pd.DataFrame(products)
print(calls, "requests,", len(df), "products")
print((~df["in_stock"]).sum(), "out of stock")
top = df.loc[df["reviews"].idxmax()]
print("Most reviewed:", top["name"], top["reviews"])
```

Output:

```text
3 requests, 120 products
20 out of stock
Most reviewed: Pro Hose Reel 894
```

**Line by line.**

- `products, page, pages, calls = [], 1, 1, 0` starts the list, the page counter, a first guess of 1 page, and the request counter.
- `while page <= pages:` stops after the last page; `pages = data["pages"]` replaces the guess with the real number after the first answer.
- `params={"page": page, "per_page": 50}` asks for page `page`, 50 products at a time.
- `calls += 1` counts the requests.
- `(~df["in_stock"]).sum()` counts the products **not** in stock: `~` reverses `True` and `False`, and summing booleans counts the `True` values.
- `df.loc[df["reviews"].idxmax()]` is the row with the most reviews.

**Reading the result.** 3 requests for 120 products (50 + 50 + 20). 20 are out of stock. The *Pro Hose Reel* has the most reviews, 894.

**Checking.** `df["id"].is_unique` is `True`: no product counted twice. Count the out-of-stock products per category: Audio 5, Garden 8, Kitchen 6 and Office 1, which add up to 20.

**Mistakes this exercise provokes.**

- `per_page=500`, hoping for one request: the API caps it at 50 and still returns 3 pages; a loop that assumed one page would keep only 50 products.
- `df["in_stock"].sum()` counts the products **in** stock, 100.
- Stopping when a page is empty instead of on `pages`: it works, but costs one extra request.

**The choice it makes.** Reading `pages` from the answer means the loop never guesses. With the default page size of 12, the same collection takes 10 requests; with 50, it takes 3. Ask for the largest page size the API allows.

### Another way to solve it

Ask for page 1 first, then loop over the remaining pages with `range`:

```python
first = session.get(url, params={"page": 1, "per_page": 50}, timeout=10).json()
products = first["products"]
for page in range(2, first["pages"] + 1):
    time.sleep(0.2)
    products += session.get(url, params={"page": page, "per_page": 50}, timeout=10).json()["products"]
```

The same three requests. The `while` version needs no special first request; the `range` version states the number of pages up front.

### A variation to try

Print the three most reviewed products:

```python
print(df.nlargest(3, "reviews")[["name", "reviews"]].to_string(index=False))
```

```text
                name  reviews
       Pro Hose Reel      894
Smart Coffee Grinder      893
       Smart Speaker      891
```

The top three are within three reviews of each other: rankings this close can change from one day to the next on a real shop.

### If your output differs

1. **`1 requests, 50 products`**: `pages` is not updated from the answer.
2. **`100 out of stock`**: the `~` is missing.

---

## Exercise 15.4 (harder)

> Write a function `all_pages(url, params)` that collects every product for any category and sort, stops on the `pages` value, and never sends more than one request per 0.2 seconds. Use it to print, for each category, the cheapest product in stock. Expected output:

**What the question asks.** A reusable function that collects every page of the product list for any combination of filters, politely, and its use: the cheapest **in-stock** product of each category.

**The plan.** `all_pages(url, params)` runs the pagination loop of exercise 15.3, adding `page` and `per_page` to whatever parameters it receives, with a pause after each request. For each category, ask for products sorted by price, keep those in stock, and take the first.

```python
import time

import pandas as pd
import requests

session = requests.Session()
URL = "http://localhost:8000/shop/api/products"


def all_pages(url, params):
    items, page, pages = [], 1, 1
    while page <= pages:
        data = session.get(
            url,
            params={**params, "page": page, "per_page": 50},
            timeout=10,
        ).json()
        items += data["products"]
        pages = data["pages"]
        page += 1
        time.sleep(0.2)
    return items


for category in ["Audio", "Garden", "Kitchen", "Office"]:
    df = pd.DataFrame(
        all_pages(URL, {"category": category, "sort": "price"})
    )
    cheapest = df[df["in_stock"]].iloc[0]
    print(
        f"{category:<8} {cheapest['name']:<20} £{cheapest['price']:.2f}"
    )
```

Output:

```text
Audio    Eco Headphones       £5.16
Garden   Eco Hose Reel        £18.78
Kitchen  Travel Scale         £14.30
Office   Mini Notebook        £5.55
```

**Line by line.**

- `{**params, "page": page, "per_page": 50}` builds a new dictionary: the caller's parameters plus the page keys. `params` itself is not changed, so the caller's dictionary stays clean.
- `time.sleep(0.2)` after each request keeps to the site's rule of at most five requests per second.
- `return items` gives back every product of every page.
- For each category, `{"category": category, "sort": "price"}` asks for that category, cheapest first.
- `df[df["in_stock"]]` keeps the products in stock; `.iloc[0]` takes the first row by position, the cheapest available.
- The f-string aligns the category in 8 characters and the name in 20, and writes the price with two decimals.

**Reading the result.** Audio and Office both have an in-stock product under £6: *Eco Headphones* at £5.16 and *Mini Notebook* at £5.55. In Garden, the cheapest product is out of stock, so the answer is the next one, *Eco Hose Reel* at £18.78.

**Checking.** Ask for the Garden category sorted by price: the first product, *Mini Watering Can*, has `in_stock` `False`, which is why it is skipped. Compare with the pandas version below: the same four lines.

**Mistakes this exercise provokes.**

- `params["page"] = page` inside the function: it changes the caller's dictionary, and the next call starts with a leftover `page`.
- `.iloc[0]` without filtering on stock first: Garden's answer is a product nobody can buy.
- `.loc[0]` instead of `.iloc[0]`: `.loc` looks for the row **labelled** 0, which after filtering may not exist.

**The choice it makes.** `{**params, "page": page}` builds a new dictionary from `params` plus the page keys, without changing `params`. Sorting on the server and filtering in Python divides the work: the API does what it offers (sorting), and you do what it does not (stock filtering).

### Another way to solve it

Collect all products once, then let pandas find the cheapest in-stock product per category:

```python
df = pd.DataFrame(all_pages(URL, {}))
in_stock = df[df["in_stock"]]
cheapest = in_stock.loc[in_stock.groupby("category")["price"].idxmin()]
print(cheapest[["category", "name", "price"]].to_string(index=False))
```

```text
category           name  price
   Audio Eco Headphones   5.16
  Garden  Eco Hose Reel  18.78
 Kitchen   Travel Scale  14.30
  Office  Mini Notebook   5.55
```

Three requests instead of nine (one per category, plus pages). When you need several answers from the same data, collect it once.

### A variation to try

Use `all_pages` to print the best-rated in-stock product of each category: `{"category": category, "sort": "rating"}`, then the first in-stock row. Watch for ties, as in exercise 15.1.

### If your output differs

1. **Garden shows a product out of stock**: the stock filter is missing or after `.iloc[0]`.
2. **`IndexError: single positional indexer is out-of-bounds`**: a category has no product in stock, or the category name is misspelt.
