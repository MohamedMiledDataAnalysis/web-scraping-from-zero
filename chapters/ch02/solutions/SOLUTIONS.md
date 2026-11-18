# Chapter 2 — detailed solutions

These are the solutions printed in the book, word for word: what the question asks, the plan, the code, line by line, reading the result, checking, the mistakes the exercise provokes, the choice it makes, another way to solve it, a variation to try, and what to do if your output differs. Here, each program is followed by its exact output.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 2.1 (easy)

> `raw = "  Out of stock \n"`. Print the cleaned text in lower case, then print `True` if the word `out` is in it. Expected output:

**What the question asks.** Clean a piece of scraped text (remove the spaces and the line break around it, and put it in lower case), then test whether a word appears in it.

**The plan.** Chain two string methods, `strip()` then `lower()`, keep the result, and use `in` to search it.

```python
raw = "  Out of stock \n"
clean = raw.strip().lower()
print(clean)
print("out" in clean)
```

Output:

```text
out of stock
True
```

**Line by line.**

- `raw = "  Out of stock \n"` is the text as a page often gives it: spaces before, a space and a line break (`\n`) after.
- `raw.strip()` returns a **new** string without the spaces and line breaks at both ends: `"Out of stock"`. `raw` itself does not change.
- `.lower()` acts on that new string and returns `"out of stock"`. Calling methods one after the other like this is called *chaining*.
- `clean = ...` keeps the result.
- `"out" in clean` asks whether the text `out` appears anywhere inside `clean`; the answer is `True` or `False`.

**Reading the result.** The first line has no visible spaces around it and no empty line after it: the line break is gone. The second line, `True`, is a *boolean*, Python's yes-or-no value.

**Checking.** `print(repr(clean))` shows the exact text with its quotes: `'out of stock'`, with no space at either end. `repr` is the tool to see hidden spaces and line breaks.

**Mistakes this exercise provokes.**

- `"out" in raw` gives `False`: `raw` contains `Out` with a capital O, and `in` is exact. Lower the case before you search for a word.
- `raw.strip()` on its own line, without keeping the result: `raw` is unchanged, because strings never change in place.
- `raw.lower().strip` without brackets: you get the method itself, printed as `<built-in method strip ...>`, not the text.

**The choice it makes.** Here the order of `strip()` and `lower()` does not matter: either gives the same result. With `replace` and `float`, order matters, as exercise 2.3 shows.

**Another way to solve it.** `casefold()` is a stronger version of `lower()`, made for comparing text in any language (it turns the German `ß` into `ss`, for example):

```python
print(raw.strip().casefold())
```

```text
out of stock
```

For English text, `lower()` and `casefold()` give the same result. Use `casefold()` when you compare words from international sites.

**A variation to try.** Test a word that is in the text with the original case: `"stock" in raw` gives `True` even without `lower()`, because `stock` is already in lower case. Then test `clean == "out of stock"`: `True`, an exact comparison of the whole text, stricter than `in`.

**If your output differs.**

1. **An empty line after `out of stock`**: you printed `raw.lower()` without `strip()`, so the `\n` is still there.
2. **`False` on the second line**: you searched `raw` instead of `clean`.

---

## Exercise 2.2 (easy)

> From the list `ratings = ["Three", "One", "Five", "Two"]`, print the number of ratings, the first one and the last one, on one line. Expected output:

**What the question asks.** Three facts about a list, printed on one line: how many items it has, its first item and its last item.

**The plan.** `len()` for the count, position 0 for the first item, position -1 for the last, and one `print` with three values.

```python
ratings = ["Three", "One", "Five", "Two"]
print(len(ratings), ratings[0], ratings[-1])
```

Output:

```text
4 Three Two
```

**Line by line.**

- `ratings = [...]` is a list of four strings. Lists keep their order.
- `len(ratings)` returns 4, the number of items.
- `ratings[0]` is the first item: positions start at 0, not 1.
- `ratings[-1]` is the last item: negative positions count from the end.
- `print(a, b, c)` prints the three values separated by spaces.

**Reading the result.** `4 Three Two`: four ratings, the first is `Three`, the last is `Two`.

**Checking.** Count the items in the list by eye: four. `print(ratings[3])` also prints `Two`, since the last of four items is at position 3.

**Mistakes this exercise provokes.**

- `ratings[1]` for the first item gives `One`, the **second** item: positions start at 0.
- `ratings[4]` for the last item stops with `IndexError: list index out of range`: four items have positions 0 to 3.
- `ratings[len(ratings)]`: the same error, for the same reason.

**The choice it makes.** `ratings[-1]` keeps working when the list grows; `ratings[3]` breaks as soon as the list has a different length. On scraped data, where you rarely know the length in advance, prefer `-1`.

**Another way to solve it.** An f-string controls the text around each value:

```python
print(f"{len(ratings)} ratings, first {ratings[0]}, last {ratings[-1]}")
```

```text
4 ratings, first Three, last Two
```

Inside an f-string, any expression between `{ }` is calculated and its value inserted.

**A variation to try.** Try these and predict each result before you run it: `ratings[1:3]` gives `['One', 'Five']` (positions 1 and 2, not 3); `ratings[::-1]` gives the list reversed; `sorted(ratings)` sorts alphabetically, `['Five', 'One', 'Three', 'Two']`, which is **not** the order of the ratings. Chapter 13 turns the words into numbers to sort them properly.

**If your output differs.**

1. **`IndexError: list index out of range`**: a position is too large; the last valid position is `len(ratings) - 1`.
2. **Brackets and quotes printed**: you printed the list itself, not its items.

---

## Exercise 2.3 (medium)

> `prices = ["£26.93", " £1,049.00", "£6.56 ", "£19.20"]`. Convert every price into a number (watch the spaces and the comma), then print the list of numbers, the highest price with `max()` and the average rounded to two decimals. Expected output:

**What the question asks.** Turn four price texts, each with its own problem (spaces, a thousands comma), into numbers; then use the numbers: the list, the highest, the average rounded to pennies.

**The plan.** Loop over the prices; for each, remove the spaces, the `£` and the comma, convert with `float()`, add to a new list. Then `max()`, `sum()` and `len()` on that list.

```python
prices = ["£26.93", " £1,049.00", "£6.56 ", "£19.20"]
numbers = []
for p in prices:
    clean = p.strip().replace("£", "").replace(",", "")
    numbers.append(float(clean))
print(numbers)
print(max(numbers))
print(round(sum(numbers) / len(numbers), 2))
```

Output:

```text
[26.93, 1049.0, 6.56, 19.2]
1049.0
275.42
```

**Line by line.**

- `numbers = []` starts an empty list for the results.
- `p.strip()` removes the spaces at both ends: `" £1,049.00"` becomes `"£1,049.00"`.
- `.replace("£", "")` removes the pound sign; `.replace(",", "")` removes the thousands comma: `"1049.00"`.
- `float(clean)` converts the text into the number `1049.0`; `numbers.append(...)` adds it to the end of the list.
- `max(numbers)` returns the largest number.
- `sum(numbers) / len(numbers)` is the average; `round(..., 2)` keeps two decimals.

**Reading the result.** The list shows numbers, without quotes and without `£`: `1049.0`, not `"£1,049.00"`. The average, £275.42, is far above three of the four prices: one expensive book pulls it up.

**Checking.** Add up by hand: 26.93 + 1049 + 6.56 + 19.20 = 1101.69, divided by 4 gives 275.4225, which rounds to 275.42.

**Mistakes this exercise provokes.**

- Forgetting `.replace(",", "")` stops at the second price with `ValueError: could not convert string to float: '1,049.00'`. Python never reads a comma as a thousands separator.
- Converting before cleaning, `float(p).replace(...)`: the error happens at `float`, before the cleaning runs.
- `round(sum(numbers) / len(numbers))` without the `2`: you get `275`, a whole number.

**The choice it makes.** The same cleaning fits in one line as a *comprehension*:

```python
numbers = [float(p.strip().replace("£", "").replace(",", ""))
           for p in prices]
```

Both are correct. The loop is easier to read and to debug, because you can add `print(clean)` inside it; the comprehension is shorter. Choose the loop while you learn.

**Another way to solve it.** `float()` accepts spaces around a number: `float(" 6.56 ")` gives `6.56`. So `strip()` is not even needed here: removing the `£` and the comma from `" £1,049.00"` leaves `" 1049.00"`, which `float` reads as `1049.0`:

```python
numbers = [float(p.replace("£", "").replace(",", "")) for p in prices]
```

It gives the same list. Keep `strip()` anyway: it costs nothing and protects you against the line breaks that real pages add.

**A variation to try.** The average is pulled up by one expensive book. Print the average of the prices below £100 only:

```python
cheap = [n for n in numbers if n < 100]
print(round(sum(cheap) / len(cheap), 2))
```

```text
17.56
```

Then print the cheapest price with `min(numbers)` (6.56) and the list sorted with `sorted(numbers)`.

**If your output differs.**

1. **`ValueError: could not convert string to float`**: print each `clean` inside the loop to see which price still contains a character other than digits and a dot.
2. **`275.4225`**: you forgot `round(..., 2)`.
3. **French or German prices** (`1.049,00 €`): the comma is the decimal separator there, and this cleaning gives a wrong number; Chapter 13 handles both formats.

---

## Exercise 2.4 (harder)

> Print the addresses of pages 48 to 50 of the library, then the address of every **even** page from 2 to 10 on one line, separated by spaces. Hint: `range` accepts a third number, the step. Expected output:

**What the question asks.** Build page addresses with numbers in them: three consecutive pages, one address per line, then every even page from 2 to 10 on a single line.

**The plan.** `range()` produces the numbers; an f-string puts each number into the address; `" ".join()` glues a list of texts into one line.

```python
for page in range(48, 51):
    print(f"http://localhost:8000/library/page-{page}.html")

even = [f"page-{n}.html" for n in range(2, 11, 2)]
print(" ".join(even))
```

Output:

```text
http://localhost:8000/library/page-48.html
http://localhost:8000/library/page-49.html
http://localhost:8000/library/page-50.html
page-2.html page-4.html page-6.html page-8.html page-10.html
```

**Line by line.**

- `range(48, 51)` gives 48, 49, 50: it starts at the first number and stops **before** the second.
- `f"...page-{page}.html"` inserts the current number into the address.
- `range(2, 11, 2)` gives 2, 4, 6, 8, 10: the third number is the step. 11 is excluded, so 10 is the last.
- `[f"page-{n}.html" for n in range(2, 11, 2)]` builds a list of five texts.
- `" ".join(even)` returns one string: the five texts with a space between each. It is the opposite of `split`.

**Reading the result.** Three full addresses, then one line with five page names. Each address is exactly what the browser shows for that page.

**Checking.** Paste the first address into the browser: page 48 of the library opens. Count the items on the last line: five.

**Mistakes this exercise provokes.**

- `range(48, 50)` misses page 50. When you want the last number included, add 1 to it.
- `range(2, 10, 2)` stops at 8, for the same reason.
- `" ".join(range(2, 11, 2))` stops with `TypeError: sequence item 0: expected str instance, int found`: `join` only glues text, so convert the numbers first.
- `"page-{n}.html"` without the `f`: every item is the text `page-{n}.html`, braces included.

**The choice it makes.** Building addresses from a number is how every scraper in Part 3 walks through pages. `range` makes the first and last page explicit, which is what you check first when a scraper misses data.

**Another way to solve it.** Count down from page 50 with a negative step:

```python
for page in range(50, 47, -1):
    print(f"http://localhost:8000/library/page-{page}.html")
```

The pages come out as 50, 49, 48. With a negative step, the stop number must be **smaller** than the start.

**A variation to try.** Join with a comma and a space instead of a space:

```python
print(", ".join(f"page-{n}.html" for n in range(1, 4)))
```

```text
page-1.html, page-2.html, page-3.html
```

The text before `.join` is the separator; it can be anything, including `"\n"`, which puts each item on its own line.

**If your output differs.**

1. **One page missing at the end**: the stop number of `range` is excluded; add 1.
2. **`TypeError: sequence item 0: expected str instance, int found`**: you joined numbers; turn them into text with an f-string or `str(n)`.
3. **The page names on separate lines**: you printed inside the loop instead of joining the list.
