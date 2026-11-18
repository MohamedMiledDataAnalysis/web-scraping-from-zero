# Chapter 14 — detailed solutions

These are the solutions printed in the book, word for word: what the question asks, the plan, the code, line by line, reading the result, checking, the mistakes the exercise provokes, the choice it makes, another way to solve it, a variation to try, and what to do if your output differs. Here, each program is followed by its exact output.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 14.1 (easy)

> Print the names of the UK stations, using the `country` parameter. Expected output:

**What the question asks.** Ask the open API for the stations of one country, the United Kingdom, by passing a parameter, and print their names.

**The plan.** One `GET` request to `/api/v1/stations` with the API key in the `X-API-Key` header and `country=UK` as a parameter; read the JSON answer and take each station's `name`.

```python
import requests

r = requests.get("http://localhost:8000/api/v1/stations",
                 headers={"X-API-Key": "pg-demo-2027"},
                 params={"country": "UK"}, timeout=10)
r.raise_for_status()
print([s["name"] for s in r.json()["stations"]])
```

Output:

```text
['London Riverside', 'Manchester Hill', 'Edinburgh Port']
```

**Line by line.**

- `headers={"X-API-Key": "pg-demo-2027"}` sends the key the API requires; the Practice Ground's demo key is printed in its documentation page.
- `params={"country": "UK"}` adds `?country=UK` to the address.
- `r.raise_for_status()` stops the program at once if the API refused the request.
- `r.json()` turns the answer into Python: a dictionary with the keys `count` and `stations`.
- `[s["name"] for s in r.json()["stations"]]` takes the name of each station.

**Reading the result.** Three UK stations: London Riverside, Manchester Hill and Edinburgh Port. The API filtered them; the program did no filtering itself.

**Checking.** Remove `params` and run again: five stations, three in the UK and two in France. `print(r.json()["stations"][0])` shows all the fields of a station: `id`, `name`, `country`, `lat`, `lon`.

**Mistakes this exercise provokes.**

- Forgetting the header: the API answers 401 with `{'error': 'Missing API key. Send it in the X-API-Key header.'}`, and `raise_for_status()` stops the program.
- `country=uk` in lower case: status 200 and an empty list, because the API compares codes exactly. No error tells you; check the count.
- Putting the key in `params` instead of `headers`: the same 401. Each API documents where it expects its key.

**The choice it makes.** Asking the API to filter (`country=UK`) means less data travels and no filtering code. Filter in Python only when the API offers no parameter for it.

**Another way to solve it.** Ask for all stations and filter in Python:

```python
r = requests.get("http://localhost:8000/api/v1/stations",
                 headers={"X-API-Key": "pg-demo-2027"}, timeout=10)
print([s["name"] for s in r.json()["stations"] if s["country"] == "UK"])
```

The same three names. Fine for five stations; for thousands, let the API filter.

**A variation to try.** Print each UK station with its coordinates: `f'{s["id"]} {s["name"]} ({s["lat"]}, {s["lon"]})'`. London is `LON London Riverside (51.5, -0.12)`. These identifiers, `LON`, `MAN` and `EDI`, are the `station` values of the next exercises.

**If your output differs.**

1. **`requests.exceptions.HTTPError: 401`**: the key is missing or misspelt.
2. **An empty list**: check the case of `UK`.
3. **`HTTPError: 429`**: you ran many requests in a few seconds; wait 10 seconds and try again.

---

## Exercise 14.2 (medium)

> Collect the observations of London (`LON`) for February 2027, all pages, and print the number of days, the warmest maximum temperature and its date. Expected output:

**What the question asks.** All the daily observations of London for February 2027, which the API spreads over several pages, then three facts: how many days, the warmest maximum temperature, and its date.

**The plan.** A pagination loop driven by the API's `next` field: request the first page with the parameters; then follow `next` until it is empty. Collect every result, build a DataFrame, find the row with the highest maximum.

```python
from urllib.parse import urljoin

import pandas as pd
import requests

BASE = "http://localhost:8000"
session = requests.Session()
session.headers["X-API-Key"] = "pg-demo-2027"
url = BASE + "/api/v1/observations"
params = {"station": "LON", "start": "2027-02-01", "end": "2027-02-28"}
rows = []
while url:
    data = session.get(url, params=params, timeout=10).json()
    rows += data["results"]
    url = urljoin(BASE, data["next"]) if data["next"] else None
    params = None
df = pd.DataFrame(rows)
warmest = df.loc[df["temp_max_c"].idxmax()]
print(
    len(df),
    "days; warmest:",
    warmest["temp_max_c"],
    "on",
    warmest["date"],
)
```

Output:

```text
28 days; warmest: 11.1 on 2027-02-18
```

**Line by line.**

- `session.headers["X-API-Key"] = ...` sets the key once for every request of the session.
- The first request sends `station`, `start` and `end` as parameters.
- `data["results"]` holds up to 10 observations; `rows += ...` adds them to the list.
- `data["next"]` is the address of the next page, such as `/api/v1/observations?station=LON&...&page=2`, or `None` on the last page; `urljoin(BASE, ...)` makes it complete.
- `params = None` after the first request: the `next` address already contains every parameter, and sending them again would duplicate them.
- `df["temp_max_c"].idxmax()` gives the index of the row with the highest maximum; `df.loc[...]` takes that row.

**Reading the result.** 28 days, the whole month, from 3 pages. The warmest day reached 11.1 °C, on 18 February.

**Checking.** `print(data["pages"])` on the first answer shows 3, and `print(data["count"])` shows 28. `df["date"].min()` and `df["date"].max()` must be the first and last day of February.

**Mistakes this exercise provokes.**

- Keeping `params` for every page: the address then holds each parameter twice, and the API may read the wrong page.
- Stopping after the first answer: 10 days instead of 28.
- `df["temp_max_c"].max()` alone gives 11.1 but not the date; `idxmax()` gives the row.

**The choice it makes.** Following `next` lets the API decide how pages work. Building `page=2`, `page=3` yourself would also work here, but breaks the day the API changes its page size or its parameter names.

**Another way to solve it.** Use the `pages` field to loop over page numbers:

```python
first = session.get(url, params=params, timeout=10).json()
rows = first["results"]
for page in range(2, first["pages"] + 1):
    rows += session.get(url, params={**params, "page": page}, timeout=10).json()["results"]
```

`{**params, "page": page}` copies the parameters and adds `page`. It makes the same three requests. Use it when an API gives the number of pages but no `next` link.

**A variation to try.** Print the five rainiest days of February: `df.nlargest(5, "rain_mm")[["date", "rain_mm"]]`. Then the number of dry days: `(df["rain_mm"] == 0).sum()`.

**If your output differs.**

1. **10 days**: the loop stops after the first page; check `url = urljoin(...)`.
2. **Duplicated days**: `params` is sent with every page; set it to `None` after the first request.
3. **`KeyError: 'results'`**: the API returned an error; print `data`.

---

## Exercise 14.3 (medium)

> Ask for the station `XYZ`, then for an end date before the start date. Print the status code and the API's error message for each. Expected output:

**What the question asks.** Provoke two errors on purpose (a station that does not exist, and an end date before the start) and read what the API says about each.

**The plan.** Two requests in a loop, each with bad parameters. Do **not** call `raise_for_status()`: the error message is in the JSON body, so read it.

```python
import requests

url = "http://localhost:8000/api/v1/observations"
headers = {"X-API-Key": "pg-demo-2027"}
for params in [
    {"station": "XYZ"},
    {"station": "LON", "start": "2027-03-01", "end": "2027-02-01"},
]:
    r = requests.get(url, params=params, headers=headers, timeout=10)
    print(r.status_code, r.json()["error"])
```

Output:

```text
400 Unknown station. See /api/v1/stations.
400 end must be after start, at most 366 days later.
```

**Line by line.**

- The list holds two dictionaries of parameters, one per bad request.
- `requests.get(url, params=params, headers=headers, ...)` sends each one with the key.
- `r.status_code` is the code; `r.json()["error"]` is the API's explanation, in its JSON body.

**Reading the result.** Both answers have status 400, *bad request*, with two different messages: `Unknown station. See /api/v1/stations.` and `end must be after start, at most 366 days later.` A good API tells you how to fix the request.

**Checking.** Try a date in the wrong format, `start=01/02/2027`: another 400, `Dates must look like 2027-01-31 and page must be a number.` Try a range longer than a year: the second message again.

**Mistakes this exercise provokes.**

- Calling `raise_for_status()` before reading the body: the program stops with `HTTPError: 400 Client Error`, and you never see the message that explains why.
- `r.text` instead of `r.json()["error"]`: you get the whole JSON as text, harder to read.
- Retrying a 400: it fails the same way every time.

**The choice it makes.** A 400 means *your request is wrong*: fix the parameters, never retry the same request. A 429 or a 5xx is different: Chapter 20 retries those.

**Another way to solve it.** Use `raise_for_status()`, but print the body when it raises:

```python
try:
    r.raise_for_status()
except requests.HTTPError:
    print(r.status_code, r.json().get("error", r.text))
```

This keeps the program's normal path strict and still shows the explanation. `.get("error", r.text)` falls back to the raw text if the body has no `error` field.

**A variation to try.** Remove the key from `headers` and run one request: status 401 with `Missing API key. Send it in the X-API-Key header.` A 401 is a refusal too: never retry it without fixing the key.

**If your output differs.**

1. **`json.decoder.JSONDecodeError`**: the answer is not JSON, often an HTML error page; print `r.text[:200]`.
2. **`429`**: wait 10 seconds; you are over the limit.

---

## Exercise 14.4 (medium)

> The hidden shop API of Chapter 15 also answers without a key: `http://localhost:8000/shop/api/products?per_page=5`. Flatten its answer with `json_normalize` and print the columns, then the names of the products in stock. Expected output:

**What the question asks.** Read a JSON list of products into a table with `json_normalize`, print its columns, then the names of the products in stock.

**The plan.** One request with `per_page=5`; `pd.json_normalize` on the `products` list; filter with the boolean column `in_stock`.

```python
import pandas as pd
import requests

data = requests.get("http://localhost:8000/shop/api/products",
                    params={"per_page": 5}, timeout=10).json()
products = pd.json_normalize(data["products"])
print(list(products.columns))
print(products.loc[products["in_stock"], "name"].tolist())
```

Output:

```text
['category', 'id', 'in_stock', 'name', 'price', 'rating', 'reviews', 'sku']
['Mini Kettle', 'Compact Kettle', 'Smart Kettle', 'Classic Kettle']
```

**Line by line.**

- `params={"per_page": 5}` asks the shop API for five products only.
- `.json()` gives a dictionary with `page`, `pages`, `products` and `total`; `data["products"]` is the list.
- `pd.json_normalize(...)` builds a DataFrame, one row per product and one column per field. For nested objects, it would flatten them into columns such as `offer.price`.
- `products.loc[products["in_stock"], "name"]` keeps the rows where `in_stock` is `True` and the `name` column.

**Reading the result.** Eight columns, sorted alphabetically by the API. Four of the five products are in stock; the fifth, the *Pro Kettle*, is not.

**Checking.** `print(products[["name", "in_stock"]])` shows the five products and their stock flags side by side. `products["in_stock"].dtype` is `bool`.

**Mistakes this exercise provokes.**

- `pd.json_normalize(data)` on the whole answer: one row with a `products` column holding the list, not five rows.
- `products[products["in_stock"] == "True"]`: an empty result, because the values are booleans, not text.
- Forgetting `.tolist()`: you print a pandas Series with its index.

**The choice it makes.** `products["in_stock"]` is already a column of `True` and `False`, so it can select rows directly. Here every product is flat, so `pd.DataFrame(data["products"])` gives the same table; `json_normalize` matters when the JSON nests objects inside objects.

**Another way to solve it.** `query` with a boolean column, and its opposite with `~`:

```python
print(products.query("in_stock")["name"].tolist())
print(products.loc[~products["in_stock"], "name"].tolist())
```

```text
['Mini Kettle', 'Compact Kettle', 'Smart Kettle', 'Classic Kettle']
['Pro Kettle']
```

`~` reverses a boolean column: `True` becomes `False`.

**A variation to try.** Ask for the second page of five products (`params={"per_page": 5, "page": 2}`) and print the cheapest product of the two pages together: `pd.concat([page1, page2]).nsmallest(1, "price")`.

**If your output differs.**

1. **One row**: you normalised the whole answer instead of `data["products"]`.
2. **An empty list**: you compared `in_stock` with a string.

---

## Exercise 14.5 (harder)

> For each of the five stations, collect the observations of the first quarter of 2027 (1 January to 31 March, 9 pages per station: 45 requests), respecting the limit with `api_get`. Print the total rainfall of each station, highest first, and the number of 429 answers you received. Expected output:

**What the question asks.** A collection that hits the API's limit if done carelessly: 45 requests (5 stations × 9 pages) under a limit of 10 requests per 10 seconds. Total rainfall per station, highest first, and how many times the API answered 429.

**The plan.** A function `api_get` that retries when the answer is 429, waiting as long as the `Retry-After` header says, and counts those answers. Around it, a loop over stations and a pagination loop, with a pause of 1.1 seconds between calls.

```python
import time
from urllib.parse import urljoin

import pandas as pd
import requests

BASE = "http://localhost:8000"
session = requests.Session()
session.headers["X-API-Key"] = "pg-demo-2027"
limited = 0


def api_get(url, params=None):
    global limited
    while True:
        r = session.get(url, params=params, timeout=10)
        if r.status_code != 429:
            r.raise_for_status()
            return r.json()
        limited += 1
        time.sleep(int(r.headers.get("Retry-After", 5)))


rows = []
for station in ["LON", "MAN", "EDI", "PAR", "LYO"]:
    url = BASE + "/api/v1/observations"
    params = {
        "station": station,
        "start": "2027-01-01",
        "end": "2027-03-31",
    }
    while url:
        data = api_get(url, params)
        rows += data["results"]
        url = urljoin(BASE, data["next"]) if data["next"] else None
        params = None
        time.sleep(1.1)

df = pd.DataFrame(rows)
print(len(df), "observations")
print(
    df.groupby("station")["rain_mm"]
    .sum()
    .round(1)
    .sort_values(ascending=False)
    .to_string()
)
print("429 answers:", limited)
```

Output:

```text
450 observations
station
LYO    326.5
PAR    291.7
EDI    270.5
MAN    232.7
LON    209.9
429 answers: 0
```

**Line by line.**

- `api_get` loops: it requests; if the status is not 429, it checks other errors and returns the JSON.
- On a 429, `limited += 1` counts it, and `time.sleep(int(r.headers.get("Retry-After", 5)))` waits the number of seconds the API asks for (5 if it does not say), then tries again.
- `global limited` lets the function change the counter defined outside it.
- For each station, the inner `while` loop follows `next` as in exercise 14.2.
- `time.sleep(1.1)` spaces the calls: at most 9 requests in any 10 seconds.
- `df.groupby("station")["rain_mm"].sum()` totals the rain per station; `.round(1)` and `.sort_values(ascending=False)` tidy and order it.

**Reading the result.** 450 observations: 5 stations × 90 days. Lyon is the wettest with 326.5 mm, London the driest with 209.9 mm. `429 answers: 0`: the pauses kept the program under the limit.

**Checking.** 90 days from 1 January to 31 March 2027, so 450 rows. The program takes about 50 seconds: 45 requests × 1.1 seconds.

**Mistakes this exercise provokes.**

- Retrying a 429 at once, without waiting: the API refuses again, and a loop without a wait can send hundreds of requests in a second.
- Ignoring `Retry-After` and waiting a fixed second: you may still be inside the blocked period.
- Catching every error and retrying it: a 400 or 401 never succeeds, and the loop never ends.

**The choice it makes.** With `time.sleep(1.1)` between calls, the program stays under the limit: 0 answers with status 429. Remove the `sleep` and run it again: it still finishes with the same totals, but the API refuses several requests on the way. Both work; the first is the polite one. `global` is fine for a counter in a short script; Chapter 20's `PoliteClient` keeps such counters inside an object instead.

**Another way to solve it.** Return the counter instead of using `global`, by making `api_get` return the number of 429 answers with the data:

```python
def api_get(url, params=None):
    refused = 0
    while True:
        r = session.get(url, params=params, timeout=10)
        if r.status_code != 429:
            r.raise_for_status()
            return r.json(), refused
        refused += 1
        time.sleep(int(r.headers.get("Retry-After", 5)))
```

The caller writes `data, refused = api_get(url, params)` and adds `refused` to its total. No variable is changed from inside the function, which makes the code easier to test.

**A variation to try.** Add the average maximum temperature per station to the table: `df.groupby("station").agg(rain=("rain_mm", "sum"), tmax=("temp_max_c", "mean")).round(1)`. Is the wettest station also the coldest?

**If your output differs.**

1. **`429 answers` greater than 0**: another program used the API at the same time, or the pause is shorter than 1 second. The totals are still right.
2. **Fewer than 450 observations**: one station's loop stopped early; print `len(rows)` after each station.
3. **The program seems frozen**: it is waiting for `Retry-After`; print a message before each `sleep`.
