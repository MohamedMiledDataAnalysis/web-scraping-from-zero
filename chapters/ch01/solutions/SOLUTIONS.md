# Chapter 1 — detailed solutions

These are the solutions printed in the book, word for word: what the question asks, the plan, the code, line by line, reading the result, checking, the mistakes the exercise provokes, the choice it makes, another way to solve it, a variation to try, and what to do if your output differs. Here, each program is followed by its exact output.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 1.1 (easy)

> Open `ex1_page2.py`, copy in the lines of `first_scraper.py` and change them to print the books of page 2 of the library. The address of page 2 is `http://localhost:8000/library/page-2.html`. Expected first three lines:

**What the question asks.** The same list as `first_scraper.py`, a price and a title per book, but for page 2 of the library instead of page 1.

**The plan.** Nothing in the program depends on which page it reads except the address. Copy the program, change the address, run it.

```python
import requests
from bs4 import BeautifulSoup

url = "http://localhost:8000/library/page-2.html"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")
for card in soup.select("article.book-card"):
    title = card.h3.a["title"]
    price = card.select_one(".price").text
    print(price, title)
```

Output:

```text
£9.35 The Compass of Salt Stations
£56.05 Meadows in the Forest
£15.62 The Market and the Harbour
£24.83 Beyond the Crimson Clockmaker
£20.79 Gardens in the Archive
£25.44 The Empty Orchard: A Novel
£15.01 The Frozen Lighthouse
£8.95 The Clockmaker and the Library
£13.87 The Last Bridge
£17.77 Maps in the Clockmaker
£33.08 The Northern Compass: A Novel
£37.02 The Compass of Crimson Kingdoms
£41.64 The Last Lantern
£54.32 Lighthouses in the Market
£44.86 The Paper Archive: A Novel
£14.57 The Bright Compass
£40.85 The Frozen Bridge: A Novel
£26.43 A River of Kingdoms
£47.04 Secret River
£43.48 Towers in the Harbour
```

**Line by line.**

- `import requests` and `from bs4 import BeautifulSoup` load the two tools: one downloads pages, the other reads them.
- `url = "http://localhost:8000/library/page-2.html"` keeps the address in a variable. The rest of the program refers to `url`, so the address appears once.
- `requests.get(url)` asks the Practice Ground for the page and returns its answer; `page.text` is the HTML of the page, as text.
- `BeautifulSoup(page.text, "html.parser")` turns that text into a tree you can search.
- `soup.select("article.book-card")` returns a list of the 20 book cards; the `for` loop takes them one by one.
- `card.h3.a["title"]` goes into the card's `<h3>`, then its `<a>` link, and reads the link's `title` attribute: the full title.
- `card.select_one(".price").text` finds the element with the class `price` inside this card and returns its text, such as `£9.35`.

**Reading the result.** Twenty lines, each a price then a title. The first is `£9.35 The Compass of Salt Stations`: a different book from page 1's first line, which shows the program really read page 2.

**Checking.** Open `http://localhost:8000/library/page-2.html` in your browser: the first card on screen is *The Compass of Salt Stations*, priced £9.35. Count the lines: 20, the number of books per page.

**Mistakes this exercise provokes.**

- Writing `http://localhost:8000/library/page-2` without `.html`. The site answers *Page not found* (status 404), the program finds no card and prints nothing. When a scraper prints nothing, open the same address in your browser first.
- Changing the address in one place but not another, when it was written twice. Keeping it in `url` avoids that.
- Forgetting to start the Practice Ground: `ConnectionError`, because nothing answers at `localhost:8000`.

**The choice it makes.** Putting the address in a variable costs one line now and saves work later: in Chapter 12 you will build this address in a loop for all 50 pages.

**Another way to solve it.** `card.h3.a["title"]` walks the tree step by step. The same element can be found with a CSS selector, which you will use more and more from Chapter 10:

```python
title = card.select_one("h3 a")["title"]
```

`"h3 a"` means *an `<a>` somewhere inside an `<h3>`*. Both lines give the same 20 titles. The selector version still works if the site later wraps the link in another tag; the step-by-step version does not.

**A variation to try.** Print page 50, the last page of the library: change the address to `page-50.html`. You get 20 books again (1,000 books in 50 pages). Then try `page-51.html`: nothing is printed, because the page does not exist. Check with `print(page.status_code)`: 200 for page 50, 404 for page 51.

**If your output differs.**

1. **Nothing is printed**: print `page.status_code`. 404 means the address is wrong; compare it letter by letter with the one above.
2. **`requests.exceptions.ConnectionError`**: the Practice Ground is not running. Start it with `python run_site.py` in another terminal.
3. **The same books as page 1**: you are still requesting `/library/` or `page-1.html`.

---

## Exercise 1.2 (easy)

> Change the program to print the number of books found on page 1, instead of the books themselves. Use `len()`. Expected output:

**What the question asks.** One number instead of a list: how many book cards page 1 contains.

**The plan.** Keep the list that `select` returns in a variable, then count its items with `len()`.

```python
import requests
from bs4 import BeautifulSoup

page = requests.get("http://localhost:8000/library/")
soup = BeautifulSoup(page.text, "html.parser")
cards = soup.select("article.book-card")
print(len(cards), "books on page 1")
```

Output:

```text
20 books on page 1
```

**Line by line.**

- `requests.get("http://localhost:8000/library/")` downloads page 1: the library's first page is at `/library/`.
- `soup.select("article.book-card")` returns a **list** of every element that matches: here, every `<article>` with the class `book-card`.
- `cards = ...` keeps that list, so you can use it more than once.
- `len(cards)` counts the items of the list.
- `print(len(cards), "books on page 1")` prints the number and the words, separated by a space.

**Reading the result.** `20 books on page 1`. The library shows 20 books per page, so the selector found every card and nothing else.

**Checking.** Count the cards on the page in your browser. Or compare with another selector that should give the same number: `len(soup.select(".price"))` also prints 20, one price per book.

**Mistakes this exercise provokes.**

- `print(len(soup))`: the length of the whole tree, a meaningless number.
- `soup.select_one("article.book-card")` then `len(...)`: `select_one` returns **one** element, not a list, and `len` then counts its children.
- A selector with a typo, such as `"article.bookcard"`: the count is 0, not an error. A count of 0 is the first sign that a selector is wrong.

**The choice it makes.** Counting first is a habit worth keeping: before extracting anything from a new page, print how many elements your selector finds. If it is 0, the selector is wrong; if it is the number the page shows, you can go on.

**Another way to solve it.** Count something else that appears once per book, such as the prices:

```python
print(len(soup.select(".price")), "prices on page 1")
```

```text
20 prices on page 1
```

When two different selectors give the same count, you can trust both. When they differ, one of them also matches something outside the book cards.

**A variation to try.** Count the cards on page 50 and on page 51 (`/library/page-50.html` and `page-51.html`). You get 20 and 0. A scraper that reads pages until it finds 0 cards knows it has passed the last page; Chapter 12 uses this.

**If your output differs.**

1. **`0 books on page 1`**: print `page.status_code` and check the selector's spelling: `article.book-card`, with a dot and a hyphen.
2. **A number other than 20**: you counted another element; print `soup.select("article.book-card")[0]` to see what one card contains.

---

## Exercise 1.3 (medium)

> Each card also contains the author, in a paragraph with the class `author`. Print the title and the author of the first five books of page 1, in the form `title | author`. Expected output:

**What the question asks.** Two pieces of information per book, the title and the author, for the first five books only, printed on one line each as `title | author`.

**The plan.** Find the cards as before, keep the first five with a slice, and inside the loop find the author with the class `author`.

```python
import requests
from bs4 import BeautifulSoup

page = requests.get("http://localhost:8000/library/")
soup = BeautifulSoup(page.text, "html.parser")
cards = soup.select("article.book-card")
for card in cards[:5]:
    title = card.h3.a["title"]
    author = card.select_one(".author").text
    print(title, "|", author)
```

Output:

```text
The Broken Forest | by Nadia Kowal
Salt Kingdom | by Omar Hartley
A River of Maps | by Yara Whitfield
A Clockmaker of Mirrors | by Margot Mendes
Beyond the Distant Kitchen | by Jonas Lindqvist
```

**Line by line.**

- `cards = soup.select("article.book-card")` keeps the list of 20 cards.
- `cards[:5]` is a *slice*: the items from the start up to (but not including) position 5, so the first five. Chapter 2 explains slices in detail.
- `card.h3.a["title"]` is the title, as in exercise 1.1.
- `card.select_one(".author").text` looks **inside this card only** for the element with the class `author` and returns its text.
- `print(title, "|", author)` prints three things separated by spaces: the title, a `|` and the author.

**Reading the result.** Five lines. The author text comes as the page shows it, with `by` in front: `by Nadia Kowal`. Cleaning such text is the subject of Chapter 13.

**Checking.** The first card on page 1 in the browser is *The Broken Forest* by Nadia Kowal. Count the lines: five.

**Mistakes this exercise provokes.**

- `card.select_one("author")` without the dot. In a selector, `.author` means *an element with the class `author`*; `author` means *an element called `<author>`*, which does not exist. `select_one` returns `None`, and `None.text` stops the program with `AttributeError: 'NoneType' object has no attribute 'text'`. This error always means *the thing you looked for was not found*.
- `soup.select_one(".author")` instead of `card.select_one(...)`: it searches the whole page and returns the first author every time, so all five lines show *Nadia Kowal*.
- `cards[5]` instead of `cards[:5]`: one card, the sixth, not five.

**The choice it makes.** Searching inside `card` rather than `soup` keeps each title with its own author. It is the pattern of every scraper in this book: find the repeated block first, then look inside each block.

**Another way to solve it.** Number the lines with `enumerate`, and remove the `by ` in front of the author with `removeprefix`:

```python
for i, card in enumerate(cards[:5], start=1):
    author = card.select_one(".author").text.removeprefix("by ")
    print(i, card.h3.a["title"], "|", author)
```

```text
1 The Broken Forest | Nadia Kowal
2 Salt Kingdom | Omar Hartley
3 A River of Maps | Yara Whitfield
4 A Clockmaker of Mirrors | Margot Mendes
5 Beyond the Distant Kitchen | Jonas Lindqvist
```

`enumerate` gives each item with its position; `start=1` counts from 1 instead of 0. `removeprefix("by ")` removes those three characters only if the text starts with them.

**A variation to try.** Print the last five books of page 1 instead of the first five: the slice `cards[-5:]` starts five items from the end.

**If your output differs.**

1. **`AttributeError: 'NoneType' object has no attribute 'text'`**: the class name is wrong or missing its dot. Print one card, `print(cards[0])`, and look for the author's class.
2. **The same author on every line**: you searched `soup` instead of `card`.
3. **Twenty lines**: you forgot the slice `[:5]`.

---

## Exercise 1.4 (harder)

> Print only the books of page 1 that cost less than £15. The price text is `£26.93`: remove the `£` with `.replace("£", "")` and turn the rest into a number with `float()`. Expected output:

**What the question asks.** A filter: only the books of page 1 that cost less than £15, which means comparing each price with a number.

**The plan.** For each card, take the price text, turn it into a number, compare it with 15, and print only when the comparison is true.

```python
import requests
from bs4 import BeautifulSoup

page = requests.get("http://localhost:8000/library/")
soup = BeautifulSoup(page.text, "html.parser")
for card in soup.select("article.book-card"):
    title = card.h3.a["title"]
    price_text = card.select_one(".price").text
    price = float(price_text.replace("£", ""))
    if price < 15:
        print(price, title)
```

Output:

```text
6.56 A River of Maps
9.52 A Station of Compasses
10.75 Notes from the Compass
12.76 Beyond the Quiet Kitchen
```

**Line by line.**

- `price_text = card.select_one(".price").text` gives text such as `"£12.76"`.
- `price_text.replace("£", "")` returns a copy of the text with every `£` replaced by nothing: `"12.76"`.
- `float(...)` turns that text into a decimal number, `12.76`, that you can compare.
- `if price < 15:` runs the indented line only when the price is below 15.
- `print(price, title)` prints the number (without `£`, since it is now a number) and the title.

**Reading the result.** Four books out of 20, from £6.56 to £12.76. The prices print without `£` and without a trailing zero where there is none: they are numbers now, not text.

**Checking.** Remove the `if` for a moment and print every price: you see 20 prices, and exactly four are below 15. Put the `if` back.

**Mistakes this exercise provokes.**

- `float(price_text)` without removing the pound sign stops with `ValueError: could not convert string to float: '£12.56'`.
- `if price_text < 15:` compares text with a number: `TypeError: '<' not supported between instances of 'str' and 'int'`.
- `if price < "15":` compares a number with text: the same `TypeError`.
- Forgetting the indentation of `print`: it then runs for every book, not only the cheap ones.

**The choice it makes.** `replace("£", "")` is enough for this page, where every price has exactly the form `£26.93`. Prices on real sites come with commas, spaces and other currencies; Chapter 13 builds a function that handles them.

**Another way to solve it.** Collect the cheap books in a list first, then sort them from cheapest to most expensive and print them:

```python
cheap = []
for card in soup.select("article.book-card"):
    price = float(card.select_one(".price").text.replace("£", ""))
    if price < 15:
        cheap.append((price, card.h3.a["title"]))
for price, title in sorted(cheap):
    print(price, title)
```

```text
6.56 A River of Maps
9.52 A Station of Compasses
10.75 Notes from the Compass
12.76 Beyond the Quiet Kitchen
```

Each item of `cheap` is a pair (a *tuple*): price, title. `sorted` sorts pairs by their first item, the price. Keeping the results in a list, instead of printing them at once, lets you sort, count or save them later.

**A variation to try.** Print the books between £15 and £20 inclusive: `if 15 <= price <= 20:`. On page 1 you get two: *Beyond the Distant Kitchen* at £18.87 and *Salt Kingdom* at £19.20.

**If your output differs.**

1. **`ValueError: could not convert string to float`**: print `repr(price_text)` to see the exact text, including any hidden space.
2. **All 20 books printed**: the `print` is not indented under the `if`.
3. **No book printed**: you wrote `>` instead of `<`, or compared with the wrong number.
