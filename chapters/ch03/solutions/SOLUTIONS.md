# Chapter 3 — detailed solutions

These are the solutions printed in the book, word for word: what the question asks, the plan, the code, line by line, reading the result, checking, the mistakes the exercise provokes, the choice it makes, another way to solve it, a variation to try, and what to do if your output differs. Here, each program is followed by its exact output.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 3.1 (easy)

> Create a dictionary for the job *Junior Data Analyst* at *Harbour Analytics* in *Leeds* with a minimum salary of 32000. Then print `Junior Data Analyst, Leeds: £32,000`. Expected output:

**What the question asks.** Store four facts about one job in a dictionary, then print three of them in a fixed sentence, with the salary written the British way: `£32,000`.

**The plan.** One dictionary with four keys; one f-string that reads three of them and formats the salary.

```python
job = {"title": "Junior Data Analyst", "company": "Harbour Analytics",
       "city": "Leeds", "salary_min": 32000}
print(f'{job["title"]}, {job["city"]}: £{job["salary_min"]:,}')
```

Output:

```text
Junior Data Analyst, Leeds: £32,000
```

**Line by line.**

- `job = {...}` creates a dictionary: each `"key": value` pair stores one fact. The salary is the number `32000`, not the text `"32,000"`.
- The dictionary is written over two lines: Python allows a line break anywhere inside brackets.
- `job["title"]` reads the value stored under the key `"title"`.
- The f-string uses single quotes outside (`f'...'`) because the keys inside use double quotes; mixing them avoids ending the string too early.
- `{job["salary_min"]:,}` inserts the salary; `:,` after the value is a *format specification* that adds a comma between thousands.

**Reading the result.** `Junior Data Analyst, Leeds: £32,000`. The comma appears only in the printed text; in the dictionary, the salary is still a number you can compare or add.

**Checking.** `print(job["salary_min"] + 1)` prints `32001`: the stored value is a number. `print(job)` shows the whole dictionary.

**Mistakes this exercise provokes.**

- `job["salary"]` with a key that does not exist stops with `KeyError: 'salary'`. Keys must match exactly.
- `"£" + job["salary_min"]` stops with `TypeError: can only concatenate str (not "int") to str`. An f-string converts for you.
- Storing the salary as `"32,000"`: it prints nicely but you can no longer calculate with it.

**The choice it makes.** Keep data as numbers and format only when you print. Chapter 13 shows what it costs to turn text such as `"£32,000"` back into a number.

**Another way to solve it.** `format(value, ",")` does the same as `:,` outside an f-string:

```python
print(job["title"] + ", " + job["city"] + ": £" + format(job["salary_min"], ","))
```

It prints the same sentence. The f-string version is shorter and easier to read; the `+` version shows that every piece must be text before it is joined.

**A variation to try.** Add a maximum salary to the dictionary, `job["salary_max"] = 40000`, then print `Junior Data Analyst, Leeds: £32,000 to £40,000`. Then read a key that may be missing without stopping the program: `job.get("salary", "not given")` returns `"not given"` instead of raising `KeyError`.

For a price with pennies, combine the comma and two decimals: `f"{1049.5:,.2f}"` gives `1,049.50`.

**If your output differs.**

1. **`£32000` without a comma**: the `:,` is missing or placed outside the braces.
2. **`SyntaxError`** on the print line: the quotes of the f-string and of the keys are the same kind; use `'` outside and `"` inside.

---

## Exercise 3.2 (medium)

> Write a function `stars_to_number(word)` that turns `"One"` to `"Five"` into 1 to 5. Use a dictionary inside the function. If the word is unknown, return `None`. Test it on `"Three"`, `"five"` (lower case!) and `"Six"`. Expected output:

**What the question asks.** A function that translates a rating word into a number, whatever its case, and that does not stop the program on an unknown word but returns `None`.

**The plan.** Inside the function, a dictionary from lower-case words to numbers; lower the word given; look it up with `.get()`, which returns `None` when the key is missing.

```python
def stars_to_number(word):
    words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
    return words.get(word.lower())


print(stars_to_number("Three"))
print(stars_to_number("five"))
print(stars_to_number("Six"))
```

Output:

```text
3
5
None
```

**Line by line.**

- `def stars_to_number(word):` defines a function with one parameter, `word`.
- `words = {"one": 1, ...}` is the translation table. Its keys are all in lower case.
- `word.lower()` lowers the word received, so `"Three"`, `"three"` and `"THREE"` all become `"three"`.
- `words.get(...)` returns the value for that key, or `None` if the key is not in the dictionary.
- `return` sends that value back to the line that called the function.
- The three `print` lines call the function with the three test words.

**Reading the result.** `3`, `5`, `None`: `Three` and `five` are found despite their different cases; `Six` is not a rating, and the function says so with `None` instead of crashing.

**Checking.** Test all five words in one line: `print([stars_to_number(w) for w in ["One", "Two", "Three", "Four", "Five"]])` prints `[1, 2, 3, 4, 5]`.

**Mistakes this exercise provokes.**

- `return words[word]` works for `"Three"` only if the keys have a capital letter, and stops with `KeyError: 'five'` (or `'Three'` with lower-case keys) before it even reaches `"Six"`.
- Keys with capitals (`"Three": 3`) **and** `word.lower()`: no key ever matches, and every call returns `None`.
- `print` instead of `return` inside the function: the number is shown, but the caller receives `None` and cannot use it.

**The choice it makes.** Returning `None` for an unknown word lets a scraper continue and mark the gap. You will use this function in Chapter 11, because the library writes ratings as the class `star-rating Three`.

**Another way to solve it.** A list of words in order, where the position gives the number:

```python
def stars_to_number(word):
    order = ["one", "two", "three", "four", "five"]
    w = word.lower()
    return order.index(w) + 1 if w in order else None
```

`order.index("three")` is 2, so the function returns 3. The test `if w in order` is needed because `index` raises `ValueError` on a missing word. The dictionary version is clearer and does not depend on the order of the list.

**A variation to try.** Make the function tolerate spaces as well as case: `words.get(word.strip().lower())`. Then `stars_to_number(" Four ")` returns `4`. Text scraped from pages often carries such spaces.

**If your output differs.**

1. **`None` for every word**: the dictionary keys are not in lower case.
2. **`KeyError`**: you used `words[...]` instead of `words.get(...)`.
3. **`None` printed after each number**: the function prints instead of returning, and the `print` outside prints its `None`.

---

## Exercise 3.3 (medium)

> Save the list of three quotes given in the starter file to `output/ch03/quotes.csv` with the columns `author` and `text`, then read the file back and print the number of rows and the author of the last one. Expected output:

**What the question asks.** Write a list of dictionaries to a CSV file with two named columns, read the file back, and prove it worked: the number of rows and the author of the last one.

**The plan.** Create the folder, write with `csv.DictWriter` (header first, then the rows), then read with `csv.DictReader`, which returns one dictionary per row.

```python
import csv
from pathlib import Path

quotes = [
    {
        "author": "Ada Fernhill",
        "text": "Small daily efforts build tall houses.",
    },
    {
        "author": "Walter Pike",
        "text": "Measure the wood, not your worries.",
    },
    {
        "author": "June Albright",
        "text": "Start the day with one good sentence.",
    },
]

folder = Path("output/ch03")
folder.mkdir(parents=True, exist_ok=True)
path = folder / "quotes.csv"
with open(path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["author", "text"])
    writer.writeheader()
    writer.writerows(quotes)

with open(path, encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
print(len(rows), "rows")
print(rows[-1]["author"])
```

Output:

```text
3 rows
June Albright
```

**Line by line.**

- `quotes = [...]` is a list of three dictionaries with the same two keys.
- `Path("output/ch03").mkdir(parents=True, exist_ok=True)` creates the folder, and its parent `output` if needed; `exist_ok=True` avoids an error when it already exists.
- `folder / "quotes.csv"` builds the file path; `/` joins path pieces correctly on every system.
- `open(path, "w", newline="", encoding="utf-8")` opens the file for writing. `newline=""` stops Windows from adding empty lines; `utf-8` keeps every character.
- `csv.DictWriter(f, fieldnames=["author", "text"])` writes dictionaries, taking the columns in that order.
- `writer.writeheader()` writes the first line, `author,text`; `writer.writerows(quotes)` writes one line per dictionary.
- `csv.DictReader(f)` reads the file back, using the header for the keys; `list(...)` collects all rows.
- `rows[-1]["author"]` is the author of the last row.

**Reading the result.** `3 rows` and `June Albright`: the three quotes went out and came back, in order.

**Checking.** Open `output/ch03/quotes.csv` in VS Code. The second line reads `Walter Pike,"Measure the wood, not your worries."`: the text contains a comma, so the `csv` module put it in quotes, and the comma is not read as a column separator.

**Mistakes this exercise provokes.**

- Building lines yourself with `author + "," + text`: the second quote then has three columns instead of two, and the file is broken.
- Forgetting `mkdir`: `FileNotFoundError: [Errno 2] No such file or directory`.
- Forgetting `writeheader()`: `DictReader` takes the first quote as the header, and you read 2 rows.
- Forgetting `newline=""` on Windows: an empty line between each row.

**The choice it makes.** The `csv` module handles quotes and commas for you. Chapter 13 does the same with pandas in one line; the `csv` module needs no extra package and shows what a CSV file really contains.

**Another way to solve it.** With pandas, which Chapter 7 introduces:

```python
import pandas as pd

pd.DataFrame(quotes).to_csv("output/ch03/quotes.csv", index=False)
df = pd.read_csv("output/ch03/quotes.csv")
print(len(df), "rows")
print(df.iloc[-1]["author"])
```

It prints the same two lines. `index=False` stops pandas from writing a column of row numbers; `df.iloc[-1]` is the last row.

**A variation to try.** See the classic mistake for yourself. Write the file by hand, then count the columns of each line:

```python
with open(path, "w", encoding="utf-8") as f:
    for q in quotes:
        f.write(q["author"] + "," + q["text"] + "\n")
print([len(r) for r in csv.reader(open(path, encoding="utf-8"))])
```

```text
[2, 3, 2]
```

The second line has three columns: the comma inside the quote split it. Run the solution again to repair the file.

**If your output differs.**

1. **`2 rows`** and a strange author: the header is missing; check `writeheader()`.
2. **`FileNotFoundError`**: run the program from the repository folder, so that `output/ch03` is created in the right place.
3. **Accented names garbled** when you open the file in Excel: Excel may assume another encoding; Chapter 19 shows `encoding="utf-8-sig"` for files meant for Excel.

---

## Exercise 3.4 (harder)

> The starter file contains `raw = ["£24.99", "", "£ 18.50", "N/A", "£1,049.00"]`. Write a function `safe_price(text)` that returns the price as a number, or `None` when the text is not a price. Print the list of results and the number of prices that could not be read. Expected output:

**What the question asks.** A function that never stops the program: it returns a number when the text is a price, and `None` when it is not (an empty text, `N/A`). Then two results: the list of values, and how many could not be read.

**The plan.** Clean the text (pound sign, commas, every space), try to convert it with `float()`, and catch the error that `float()` raises on anything that is not a number.

```python
def safe_price(text):
    """Return the price as a number, or None if the text is not a price."""
    clean = text.replace("£", "").replace(",", "").replace(" ", "")
    try:
        return float(clean)
    except ValueError:
        return None


raw = ["£24.99", "", "£ 18.50", "N/A", "£1,049.00"]
prices = [safe_price(t) for t in raw]
print(prices)
print(prices.count(None), "prices could not be read")
```

Output:

```text
[24.99, None, 18.5, None, 1049.0]
2 prices could not be read
```

**Line by line.**

- The docstring under `def` says what the function returns; it is how other people, and you later, learn what a function does.
- `text.replace("£", "").replace(",", "").replace(" ", "")` removes the pound sign, the thousands comma and **every** space: `"£ 18.50"` becomes `"18.50"`.
- `try:` runs `float(clean)`. If it works, `return` sends the number back.
- `except ValueError:` runs only if `float` raised `ValueError`, which it does for `""` and `"N/A"`. The function then returns `None`.
- `[safe_price(t) for t in raw]` calls the function on every item.
- `prices.count(None)` counts how many items are `None`.

**Reading the result.** `[24.99, None, 18.5, None, 1049.0]`: the list keeps five positions, one per input, with `None` where a price could not be read. `2 prices could not be read` tells you how big the hole is.

**Checking.** Five inputs, five outputs: `len(prices) == len(raw)` is `True`. The two `None` are at positions 1 and 3, where `raw` has `""` and `"N/A"`.

**Mistakes this exercise provokes.**

- `.strip()` instead of `.replace(" ", "")`: `strip` cleans only the two ends; applied before removing `£`, it would not reach the space between `£` and `18.50`.
- `except:` with no error name catches everything, including mistakes in your own code, such as a misspelt variable. Name the error you expect.
- Skipping bad items with `continue` instead of returning `None`: the list shrinks to three items, and you no longer know which inputs failed.

**The choice it makes.** Returning `None` keeps the row and marks the hole; skipping the item would lose the title and the other fields. In scraping, keep the row and mark the missing value: you can remove it later, but you cannot get it back without scraping again.

**Another way to solve it.** Keep the prices that were read, and list the texts that were not, with `zip`, which walks two lists side by side:

```python
ok = [p for p in prices if p is not None]
failed = [t for t, p in zip(raw, prices) if p is None]
print(ok, sum(ok))
print(failed)
```

```text
[24.99, 18.5, 1049.0] 1092.49
['', 'N/A']
```

Write `is not None`, not `!= None`: it is the correct test for `None`, and it also keeps a price of `0.0`, which a test such as `if p` would drop.

**A variation to try.** Predict, then check, what `safe_price` returns for `"Free"`, `"£12.50 each"`, `"12.50 GBP"` and `"€9.99"`. All four return `None`: the function only removes `£`, commas and spaces. Now try `safe_price("nan")`: it returns `nan`, a float meaning *not a number*, because `float("nan")` is valid Python. A real price cleaner must reject it; Chapter 13 builds one with a regular expression, which only accepts digits.

**If your output differs.**

1. **`[24.99, None, None, None, 1049.0]`**: the space inside `"£ 18.50"` was not removed; use `.replace(" ", "")`.
2. **The program stops with `ValueError`**: the `try` does not cover the `float(...)` line, or the `except` names another error.
3. **`0 prices could not be read`**: you removed the `None` values before counting.
