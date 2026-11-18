# Chapter 9 — detailed solutions

These are the long versions of the solutions printed in the book. Each has the same parts as the book, with more detail, plus parts the book has no room for: another way to solve the exercise, a variation to try, and what to do if your output differs.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 9.1 (easy)

> Print the text of every tag in the *Tags* box on the right of `http://localhost:8000/quotes/` (the `aside` with the class `tag-box`), on one line separated by commas. Expected output:

**What the question asks.** The 16 tags listed in the *Tags* box on the right of the quotes page, on one line, separated by commas.

**The plan.** Find the box first, the `aside` with the class `tag-box`; then find the links with the class `tag` **inside it**; join their texts.

```python
import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/quotes/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
box = soup.find("aside", class_="tag-box")
print(", ".join(a.text for a in box.find_all("a", class_="tag")))
```

Output:

```text
courage, curiosity, failure, friendship, generosity, habits, hope, humour, kindness, learning, patience, questions, reading, sea, time, work
```

**Line by line.**

- `soup.find("aside", class_="tag-box")` returns the first `aside` whose classes include `tag-box`. `class_` has an underscore because `class` is a reserved word in Python.
- `box.find_all("a", class_="tag")` searches inside `box` only and returns its 16 tag links.
- `a.text for a in ...` gives the text of each link; written inside `join(...)` without square brackets, it is a *generator expression*, which `join` reads directly.
- `", ".join(...)` glues the texts with a comma and a space between them.

**Reading the result.** Sixteen words, from `courage` to `work`, in the order the box shows them (alphabetical here).

**Checking.** Count the tags in the box on screen: 16. Then compare `len(soup.find_all("a", class_="tag"))`, which counts every tag link on the page: 36.

**Mistakes this exercise provokes.**

- `soup.find_all("a", class_="tag")` without the box: the quotes also contain links with the class `tag`, so you get 36 words, the 20 tags of the quotes mixed with the 16 of the box.
- `soup.find("aside", class="tag-box")`: `SyntaxError`, because `class` cannot be used as an argument name.
- `print(box.find_all(...))`: a list of whole tags, not their text.

**The choice it makes.** Searching inside `box` matters: find the container first, then search inside it. It is the same pattern as the book cards of Chapter 1.

### Another way to solve it

With a CSS selector, which Chapter 10 covers, the container and the links fit in one string:

```python
print(", ".join(a.text for a in soup.select("aside.tag-box a.tag")))
```

`aside.tag-box a.tag` means *links with the class `tag`, somewhere inside an `aside` with the class `tag-box`*. It prints the same 16 tags.

### A variation to try

Count the tags used by the quotes of page 1, most frequent first, with `Counter` from the standard library:

```python
from collections import Counter

print(Counter(a.text for a in soup.select("div.quote a.tag")).most_common(3))
```

```text
[('work', 3), ('courage', 2), ('failure', 2)]
```

### If your output differs

1. **36 words**: you searched the whole page instead of the box.
2. **`AttributeError: 'NoneType' object has no attribute 'find_all'`**: the box was not found; check `aside` and `tag-box`.

---

## Exercise 9.2 (easy)

> On the author page `http://localhost:8000/quotes/author/tomas-reyna/`, print the author's name, birth year and birthplace. Expected output:

**What the question asks.** Three facts from an author page (name, birth year, birthplace), printed in one sentence.

**The plan.** Each fact sits in its own element with its own class: `h1.author-title`, `span.author-born-date`, `span.author-born-location`. Find each, take its text, and build the sentence with an f-string.

```python
import requests
from bs4 import BeautifulSoup

url = "http://localhost:8000/quotes/author/tomas-reyna/"
soup = BeautifulSoup(requests.get(url, timeout=10).text, "html.parser")
name = soup.find("h1", class_="author-title").text
born = soup.find("span", class_="author-born-date").text
place = soup.find("span", class_="author-born-location").text
print(f"{name}, born {born} in {place}")
```

Output:

```text
Tomas Reyna, born 1902 in Valparaiso, Chile
```

**Line by line.**

- `soup.find("h1", class_="author-title")` returns the heading that holds the name.
- `soup.find("span", class_="author-born-date")` and `...author-born-location` return the two `span` elements of the birth line.
- `.text` takes the text of each element.
- The f-string puts the three values into the sentence.

**Reading the result.** `Tomas Reyna, born 1902 in Valparaiso, Chile`. The comma in `Valparaiso, Chile` comes from the page; the other commas come from your f-string.

**Checking.** Open the author page: the name is the big heading, and the birth line shows 1902 and Valparaiso, Chile. Print `repr(place)` to make sure there is no hidden space.

**Mistakes this exercise provokes.**

- Reading the whole birth line and cutting it with `split(",")`: the birthplace itself contains a comma, so the pieces come out wrong. Use the two `span` elements the page provides.
- `soup.find("span")` without a class: the first `span` of the page, which is not the date.
- Forgetting `.text`: the f-string inserts the whole tag, `<h1 class="author-title">Tomas Reyna</h1>`.

**The choice it makes.** When a page gives each fact its own element and class, use them: the scraper keeps working if the sentence around them changes.

### Another way to solve it

`select_one` with a class selector is shorter when the tag name does not matter:

```python
name = soup.select_one(".author-title").text
born = soup.select_one(".author-born-date").text
place = soup.select_one(".author-born-location").text
```

The result is the same. Naming the tag, as the book does, protects against another element with the same class.

### A variation to try

Add the author's description, in the element with the class `author-description`, and print its first 50 characters: `soup.select_one(".author-description").text[:50]`. For Tomas Reyna it starts *Tomas Reyna was a sailor and poet who wrote about*.

### If your output differs

1. **`AttributeError: 'NoneType' object has no attribute 'text'`**: one of the three classes is misspelt; print `soup.find("div", class_="author-details")` to see them.
2. **Extra spaces in the sentence**: print `repr` of each value and add `.strip()` where needed.

---

## Exercise 9.3 (medium)

> For each quote of page 1 of the quotes, print the author and the address of the author's *about* page, made complete with `urljoin`. Expected first three lines:

**What the question asks.** For each of the ten quotes of page 1, the author's name and the complete address of the author's *about* page.

**The plan.** Loop over the `div.quote` blocks. In each, the name is in `small.author`; the link has no class, but sits inside `span.by`, so find the `span` first, then its `a`. Make the address complete with `urljoin`.

```python
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

url = "http://localhost:8000/quotes/"
soup = BeautifulSoup(requests.get(url, timeout=10).text, "html.parser")
for q in soup.find_all("div", class_="quote"):
    author = q.find("small", class_="author").text
    about = q.find("span", class_="by").find("a")["href"]
    print(author, urljoin(url, about))
```

Output:

```text
Tomas Reyna http://localhost:8000/quotes/author/tomas-reyna/
Walter Pike http://localhost:8000/quotes/author/walter-pike/
Mira Okonkwo http://localhost:8000/quotes/author/mira-okonkwo/
Henrik Sall http://localhost:8000/quotes/author/henrik-sall/
Henrik Sall http://localhost:8000/quotes/author/henrik-sall/
Mira Okonkwo http://localhost:8000/quotes/author/mira-okonkwo/
Celeste Moreau http://localhost:8000/quotes/author/celeste-moreau/
June Albright http://localhost:8000/quotes/author/june-albright/
Tomas Reyna http://localhost:8000/quotes/author/tomas-reyna/
Mira Okonkwo http://localhost:8000/quotes/author/mira-okonkwo/
```

**Line by line.**

- `soup.find_all("div", class_="quote")` returns the ten quote blocks.
- `q.find("small", class_="author").text` is the author's name.
- `q.find("span", class_="by").find("a")` goes into the `span` with the class `by`, then finds the `a` inside it.
- `["href"]` reads the link's address, such as `/quotes/author/tomas-reyna/`, which starts with `/`.
- `urljoin(url, about)` adds the scheme and host: `http://localhost:8000/quotes/author/tomas-reyna/`.

**Reading the result.** Ten lines, one per quote. Some authors appear several times (Mira Okonkwo three times), because they wrote several of the quotes on the page.

**Checking.** Click *(about)* under the first quote in the browser: the address bar shows the first printed address.

**Mistakes this exercise provokes.**

- `q.find("a")`: the first link of the quote block, which is a **tag** link, not the *about* link.
- Printing `about` without `urljoin`: `/quotes/author/...`, which `requests` cannot open on its own.
- `soup.find("span", class_="by")` instead of `q.find(...)`: the first quote's link, repeated ten times.

**The choice it makes.** The *about* link has no class. You reach it from its parent, the `span` with the class `by`: when the element you want has no handle, find the nearest one that has. Chapter 12 follows these links to collect every author's details.

### Another way to solve it

A CSS selector can describe the path in one string: `q.select_one("span.by a")["href"]`. It gives the same address.

### A variation to try

Collect each author **once**, with a dictionary whose keys are the names:

```python
abouts = {}
for q in soup.find_all("div", class_="quote"):
    name = q.find("small", class_="author").text
    abouts[name] = urljoin(url, q.select_one("span.by a")["href"])
print(len(abouts), list(abouts)[:3])
```

```text
6 ['Tomas Reyna', 'Walter Pike', 'Mira Okonkwo']
```

Six different authors on page 1. A dictionary keeps one entry per key: a second quote by the same author overwrites the same entry. This is the list of pages Chapter 12's crawler visits.

### If your output differs

1. **Tag addresses such as `/quotes/tag/...`**: you took the first `a` of the quote.
2. **Ten identical lines**: you searched `soup` instead of `q`.

---

## Exercise 9.4 (medium)

> On page 1 of the library, count the books per rating (`One` to `Five`), using the second class of the `star-rating` paragraph. Print the counts in the order One to Five. Expected output:

**What the question asks.** How many of the 20 books of page 1 have each rating, from One to Five, read from the second class of the rating paragraph (`<p class="star-rating Three">`).

**The plan.** Prepare a dictionary with the five words in order and a count of 0. For each `p.star-rating`, take its second class and add 1 to that word's count.

```python
import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/library/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
counts = {w: 0 for w in ["One", "Two", "Three", "Four", "Five"]}
for p in soup.find_all("p", class_="star-rating"):
    word = p["class"][1]
    counts[word] += 1
print(counts)
```

Output:

```text
{'One': 5, 'Two': 1, 'Three': 5, 'Four': 3, 'Five': 6}
```

**Line by line.**

- `{w: 0 for w in [...]}` builds `{'One': 0, 'Two': 0, 'Three': 0, 'Four': 0, 'Five': 0}`.
- `soup.find_all("p", class_="star-rating")` returns the 20 rating paragraphs; BeautifulSoup matches the class even though each paragraph has two.
- `p["class"]` is a **list** of classes, such as `['star-rating', 'Three']`; `[1]` takes the second.
- `counts[word] += 1` adds 1 to that word's count.

**Reading the result.** `{'One': 5, 'Two': 1, 'Three': 5, 'Four': 3, 'Five': 6}`. The counts add up to 20, one per book, and Five stars is the most common rating on page 1.

**Checking.** `print(sum(counts.values()))` prints 20. Count the five-star books on the page by eye: six.

**Mistakes this exercise provokes.**

- `p["class"] == "Three"` is never true: `p["class"]` is a list. Take the item with `[1]`, or test `"Three" in p["class"]`.
- Starting with an empty dictionary and writing `counts[word] += 1`: `KeyError` on the first word, because the key does not exist yet.
- `p["class"][0]`: `star-rating` every time.

**The choice it makes.** Building the dictionary first with the five words in order guarantees the printing order and gives 0 to a rating that does not appear. `Counter` (below) is shorter but prints the words in another order.

### Another way to solve it

`Counter` counts for you:

```python
from collections import Counter

print(Counter(p["class"][1] for p in soup.find_all("p", class_="star-rating")))
```

```text
Counter({'Five': 6, 'Three': 5, 'One': 5, 'Four': 3, 'Two': 1})
```

The counts are the same; `Counter` lists them from the most common. A rating with no book would be missing instead of showing 0.

### A variation to try

Count one rating directly with a selector that requires both classes: `len(soup.select("p.star-rating.Three"))` gives 5. Two classes written together, without a space, mean *an element with both classes*.

### If your output differs

1. **`KeyError`**: the dictionary was not prepared with the five words, or a word is spelt differently on the page.
2. **All counts at 0**: the test compares the list with a word; use `[1]`.

---

## Exercise 9.5 (harder)

> Build a dictionary of the information table of the book `the-broken-forest-1`, then print the stock as a number (from `In stock (19 available)`) and the number of pages as a number. Expected output:

**What the question asks.** Turn a two-column information table (labels on the left, values on the right) into a dictionary, then extract two numbers from it: the stock, hidden in the text `In stock (19 available)`, and the number of pages.

**The plan.** One dictionary comprehension: for each row, the `th` text is the key and the `td` text the value. Then cut the availability text to reach the number, and convert both values with `int`.

```python
import requests
from bs4 import BeautifulSoup

url = "http://localhost:8000/library/book/the-broken-forest-1.html"
soup = BeautifulSoup(requests.get(url, timeout=10).text, "html.parser")
info = {row.th.text: row.td.text
        for row in soup.find("table", class_="info").find_all("tr")}
stock = int(info["Availability"].split("(")[1].split()[0])
pages = int(info["Pages"])
print(stock, pages)
```

Output:

```text
19 486
```

**Line by line.**

- `soup.find("table", class_="info").find_all("tr")` returns the six rows of the table.
- `{row.th.text: row.td.text for row in ...}` is a **dictionary comprehension**: one `key: value` pair per row.
- `info["Availability"]` is `In stock (19 available)`.
- `.split("(")[1]` gives `19 available)`; `.split()[0]` (split on spaces) gives `19`; `int` converts it.
- `int(info["Pages"])` converts `486`.

**Reading the result.** `19 486`: 19 copies in stock, 486 pages, both as numbers.

**Checking.** `print(info)` shows the whole dictionary, with six keys from `UPC` to `Year`. Open the book page: the table shows the same values.

**Mistakes this exercise provokes.**

- `info["availability"]` in lower case: `KeyError`; keys are copied exactly from the page.
- `int(info["Availability"])`: `ValueError: invalid literal for int() with base 10: 'In stock (19 available)'`.
- `soup.find_all("td")` alone, without the `th`: you lose which value belongs to which label, and the order of rows may change between pages.

**The choice it makes.** Splitting text works while the wording stays the same. Chapter 13 shows a regular expression, `\d+`, which finds the number wherever it is in the text. For an out-of-stock book, the text is `Out of stock (0 available)`, and both methods give 0.

### Another way to solve it

Find one value by its label, without building the dictionary:

```python
pages = soup.find("th", string="Pages").find_next_sibling("td").text
```

`string="Pages"` finds the `th` whose text is exactly `Pages`; `find_next_sibling("td")` moves to the cell next to it. Handy for one value; the dictionary is better when you need several.

The regular-expression version of the stock, from Chapter 13:

```python
import re

stock = int(re.search(r"\d+", info["Availability"]).group())
```

It also gives 19, and keeps working if the site writes `19 in stock`.

### A variation to try

Convert the price as well: `float(info["Price"].removeprefix("£"))` gives 26.93. Then build a cleaned dictionary of the three numbers with their own keys.

### If your output differs

1. **`KeyError`**: print `info.keys()` and copy the exact label.
2. **`AttributeError: 'NoneType' object has no attribute 'text'`**: a row has no `th` or no `td`; print each row.
