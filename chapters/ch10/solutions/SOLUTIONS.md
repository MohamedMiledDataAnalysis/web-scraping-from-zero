# Chapter 10 — detailed solutions

These are the solutions printed in the book, word for word: what the question asks, the plan, the code, line by line, reading the result, checking, the mistakes the exercise provokes, the choice it makes, another way to solve it, a variation to try, and what to do if your output differs. Here, each program is followed by its exact output.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 10.1 (easy)

> With one `select`, print the titles (attribute `title`) of the books of page 1 that have five stars. Expected output:

**What the question asks.** The titles of the five-star books of page 1, found with **one** selector: the selector itself must choose the right cards and reach the title links.

**The plan.** Describe the cards you want (`article.book-card` that **contains** a paragraph with the classes `star-rating` and `Five`), then go down to their title links (`h3 a`). `:has()` expresses *contains*.

```python
import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/library/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
for a in soup.select("article.book-card:has(.star-rating.Five) h3 a"):
    print(a["title"])
```

Output:

```text
A Clockmaker of Mirrors
Painted Bridge
Notes from the Compass
Beyond the Crimson Garden
Beyond the Quiet Kitchen
Notes from the Library
```

**Line by line.**

- `article.book-card` selects the book cards.
- `:has(.star-rating.Five)` keeps only the cards that contain an element with **both** classes `star-rating` and `Five` (two classes written together, with no space, mean *both on the same element*).
- ` h3 a` (after a space) goes down into those cards to their title links.
- `a["title"]` reads each link's `title` attribute, the full title.

**Reading the result.** Six titles, the same six books that exercise 9.4 counted as five stars, in the order of the page.

**Checking.** `len(soup.select("article.book-card:has(.star-rating.Five)"))` prints 6, matching the count of exercise 9.4. Change `Five` to `One`: five cards, the one-star count.

**Mistakes this exercise provokes.**

- `.star-rating.Five h3 a`: it looks for an `h3` **inside** the rating paragraph, where there is none, and prints nothing. The title is a sibling of the rating, not a child.
- `.star-rating .Five` with a space: an element with the class `Five` **inside** a `star-rating`, not the same element. No match.
- Selecting the paragraphs and printing their text: the rating paragraph holds no title.

**The choice it makes.** `:has(...)` selects an element that **contains** a match: it is the CSS way to look down before choosing. Recent browsers, BeautifulSoup, Playwright and Scrapy support it. The other way is to select the five-star paragraphs, then go up with `find_parent("article")`; `:has` keeps everything in one selector.

**Another way to solve it.** Find the rating paragraphs, then climb to their card:

```python
for p in soup.select("p.star-rating.Five"):
    print(p.find_parent("article").h3.a["title"])
```

It prints the same six titles. Useful with tools that do not support `:has`; less readable, because the selection happens in two places.

**A variation to try.** Print the titles of the one-star books (five of them, starting with *Salt Kingdom*), then count the cards that have **no** five-star rating: `len(soup.select("article.book-card:not(:has(.Five))"))` gives 14.

**If your output differs.**

1. **Nothing printed**: print `len(soup.select("p.star-rating.Five"))`; if it is 6, the problem is the part after `:has(...)`.
2. **`NotImplementedError` or a selector error**: your `soupsieve` package is very old; run `pip install -r requirements.txt` again.

---

## Exercise 10.2 (easy)

> On the quotes page 1, print the number of links whose address contains `/author/`, then the address of the first one. Expected output:

**What the question asks.** Select links by what their address contains (`/author/`), count them, and show the first one's address.

**The plan.** An attribute selector, `a[href*="/author/"]`, matches links whose `href` contains that text. `len()` counts; `[0]["href"]` reads the first.

```python
import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/quotes/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
links = soup.select('a[href*="/author/"]')
print(len(links), links[0]["href"])
```

Output:

```text
10 /quotes/author/tomas-reyna/
```

**Line by line.**

- `'a[href*="/author/"]'` means *`a` elements whose `href` attribute contains `/author/`*. The whole selector is in single quotes so that the double quotes inside are kept.
- `soup.select(...)` returns the matching links as a list.
- `len(links)` counts them; `links[0]["href"]` is the first one's address.

**Reading the result.** `10 /quotes/author/tomas-reyna/`: ten author links, one per quote, and the first points to Tomas Reyna. The count includes repeated authors: six different authors on the page.

**Checking.** `len(set(a["href"] for a in links))` prints 6, the number of distinct authors. `soup.select("span.by a")` finds the same ten links by their position instead of their address.

**Mistakes this exercise provokes.**

- `a[href="/author/"]` with `=` instead of `*=`: an exact match, which no link has. Zero results.
- Forgetting the quotes inside the brackets when the value has a `/`: write the value in quotes, `href*="/author/"`.
- `a[href*="author"]` without the slashes: correct here, but on a real site it would also match `/authorisation/` or `/co-author/`.

**The choice it makes.** Matching on the address is robust when links have no class but follow a clear pattern. The three operators: `*=` contains, `^=` starts with, `$=` ends with.

**Another way to solve it.** `^=` (starts with) is stricter than `*=` and fits this site's addresses:

```python
print(len(soup.select('a[href^="/quotes/author/"]')))
```

It also prints 10. `$=` would select by ending: `a[href$="/"]` matches every address ending with a slash, 59 links on this page, which shows why a loose pattern is risky.

**A variation to try.** Print the distinct author addresses in order of first appearance, using a dictionary to drop repeats: `list(dict.fromkeys(a["href"] for a in links))`. Six addresses.

**If your output differs.**

1. **`0`**: check the operator, `*=`, and the quotes.
2. **`IndexError: list index out of range`** on `links[0]`: the list is empty; fix the selector first.

---

## Exercise 10.3 (medium)

> On the tables page, use a selector to print the name and diameter of the last planet of the planets table, then the third row of the rates table (header row included). Use `:last-of-type` and `:nth-of-type`. Expected output:

**What the question asks.** Position-based selection: the last row of the planets table (name and diameter only), then the third row of the rates table, counting its header row.

**The plan.** `:last-of-type` picks the last `tr` of the planets body; inside it, `td:nth-of-type(1)` and `td:nth-of-type(3)` pick the first and third cells. For the rates table, anchor on its id and use `tr:nth-of-type(3)`.

```python
import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/tables/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
last = soup.select_one("#planets-table tbody tr:last-of-type")
print(
    [
        td.text
        for td in last.select("td:nth-of-type(1), td:nth-of-type(3)")
    ]
)
row = soup.select_one("#rates-table tr:nth-of-type(3)")
print(row.get_text(" | ", strip=True))
```

Output:

```text
['Neptune', '49,528']
Northbridge Bank | Fixed 1 year | 4.05% | £1,000
```

**Line by line.**

- `#planets-table tbody tr:last-of-type` selects the last `tr` inside the planets table's body.
- `last.select("td:nth-of-type(1), td:nth-of-type(3)")` searches inside that row; the comma means *or*, so it returns the first and third cells, in page order.
- `[td.text for td in ...]` keeps their texts: the name and the diameter.
- `#rates-table tr:nth-of-type(3)` selects the third `tr` of the rates table.
- `row.get_text(" | ", strip=True)` joins the texts of the row's cells with ` | ` and removes surrounding spaces.

**Reading the result.** `['Neptune', '49,528']`: the last planet and its diameter in kilometres. Then `Northbridge Bank | Fixed 1 year | 4.05% | £1,000`: the second account, because row 1 is the header.

**Checking.** Print the whole last row, `last.get_text("|", strip=True)`: `Neptune|4,515.0|49,528|59,800`, so the diameter is the third value. Print `soup.select("#rates-table tr")[2]`: the same row as `nth-of-type(3)`, since list positions start at 0.

**Mistakes this exercise provokes.**

- `tr:nth-of-type(3)` without `#rates-table` finds the third `tr` inside **each** `thead`, `tbody` or table; `select_one` returns the one in the first table, the planets: `Earth | 149.6 | 12,756 | 365.2`. Always anchor a position on an id or a class.
- `#rates-table tbody tr`: nothing, because the rates table has no `tbody` in its HTML.
- `nth-of-type(0)`: CSS positions start at 1, unlike Python's.

**The choice it makes.** The rates table has no `thead` or `tbody` in the HTML, so its header row is a `tr` like the others and counts as row 1. Browsers **add** a `tbody` when the source has none, so the Elements panel shows one and *Copy selector* includes it, while `html.parser` and `lxml` do not (html5lib does, as Chapter 9 says): with them, `#rates-table tbody tr` finds nothing.

**Another way to solve it.** Python positions on the list `select` returns are often clearer than CSS positions:

```python
last = soup.select("#planets-table tbody tr")[-1]
cells = last.find_all("td")
print([cells[0].text, cells[2].text])
print(soup.select("#rates-table tr")[2].get_text(" | ", strip=True))
```

It prints the same two lines. `[-1]` is the last row; `[2]` is the third. Use CSS positions when the selector must work outside Python too, for example in Playwright or Scrapy.

**A variation to try.** Compare `:nth-of-type(3)` with `:nth-child(3)`: on these rows every child is a `tr`, so both give the same row. They differ when siblings of other types come first, as the reference's cheat sheet shows.

**If your output differs.**

1. **`Earth | 149.6 | ...`**: the selector is not anchored on `#rates-table`.
2. **`AttributeError: 'NoneType' ...`** on the rates row: you added `tbody`; remove it.
3. **`['Neptune', '4,515.0']`**: you took the second cell; the diameter is the third.

---

## Exercise 10.4 (medium)

> Rewrite exercise 10.1 with XPath and lxml. Expected output: the same as exercise 10.1.

**What the question asks.** The same six titles as exercise 10.1, found with XPath and lxml instead of a CSS selector.

**The plan.** Parse the page with lxml, then write one XPath expression: the `article` elements that contain a `p` whose class contains `Five`, then down to the `title` attribute of their `h3/a` link.

```python
import requests
from lxml import html as lh

page = requests.get("http://localhost:8000/library/", timeout=10)
tree = lh.fromstring(page.content)
for title in tree.xpath(
    '//article[.//p[contains(@class, "Five")]]//h3/a/@title'
):
    print(title)
```

Output:

```text
A Clockmaker of Mirrors
Painted Bridge
Notes from the Compass
Beyond the Crimson Garden
Beyond the Quiet Kitchen
Notes from the Library
```

**Line by line.**

- `lh.fromstring(page.content)` parses the raw bytes into an lxml tree; giving bytes lets lxml read the page's own encoding declaration.
- `//article` finds `article` elements anywhere in the page.
- `[.//p[contains(@class, "Five")]]` is a condition: keep the `article` only if, somewhere inside it (`.//`), there is a `p` whose `class` attribute contains `Five`. The dot means *from here*.
- `//h3/a/@title` goes down to the `title` attribute of the `a` inside each kept `article`'s `h3`.
- `tree.xpath(...)` returns a list of the matching values, here strings.

**Reading the result.** The same six titles as exercise 10.1, in the same order. Two different languages, one answer.

**Checking.** `tree.xpath('count(//article[.//p[contains(@class, "Five")]])')` returns `6.0`: XPath can count by itself.

**Mistakes this exercise provokes.**

- `//p[@class="Five"]`: `@class="..."` compares the **whole** attribute, `star-rating Five`, so nothing matches. Use `contains`.
- `//article[//p[...]]` without the dot: `//p` inside the brackets searches the whole document, so every article passes the test and you get all 20 titles.
- `/@title` at the end of `//h3/a`: correct; `/title` would look for a `title` **element**, which does not exist.

**The choice it makes.** `//article[.//p[...]]` is XPath's `:has`: an `article` that has, somewhere inside it, a matching `p`. `contains(@class, "Five")` would also match a class such as `Fivefold`; the strict form below avoids that.

**Another way to solve it.** Go down to the paragraph, then **up** to its card with the `ancestor` axis, which CSS has no equivalent for:

```python
titles = tree.xpath('//p[contains(@class, "Five")]/ancestor::article//h3/a/@title')
```

It gives the same six titles. The strict class test, which matches `Five` only as a whole class name:

```python
'//article[.//p[contains(concat(" ", normalize-space(@class), " "), " Five ")]]//h3/a/@title'
```

`normalize-space` turns any run of spaces into one; adding a space at both ends lets `" Five "` match only a whole word.

**A variation to try.** Print the titles of the books that are **not** five stars: `//article[not(.//p[contains(@class, "Five")])]//h3/a/@title`. Fourteen titles.

**If your output differs.**

1. **Twenty titles**: the dot before `//p` is missing.
2. **An empty list**: you compared `@class` with `=`.
3. **`XPathEvalError: Invalid expression`**: count the brackets and the quotes.

---

## Exercise 10.5 (harder)

> With one XPath expression, print the authors of the quotes of page 1 that have the tag `work`. Expected output:

**What the question asks.** In one XPath expression, the authors of the quotes tagged `work`: a condition on a descendant (the tag), and a result elsewhere in the same block (the author).

**The plan.** Select the quote blocks that contain a tag link whose class is `tag` **and** whose text is `work`; from those blocks, go down to the author's text.

```python
import requests
from lxml import html as lh

tree = lh.fromstring(
    requests.get("http://localhost:8000/quotes/", timeout=10).content
)
authors = tree.xpath(
    '//div[@class="quote"][.//a[@class="tag" and text()="work"]]'
    '//small[@class="author"]/text()'
)
print(authors)
```

Output:

```text
['Walter Pike', 'Henrik Sall', 'Tomas Reyna']
```

**Line by line.**

- `//div[@class="quote"]` finds the quote blocks.
- `[.//a[@class="tag" and text()="work"]]` keeps the block only if it contains an `a` that has both the class `tag` and the text `work`. `and` combines two conditions inside the same brackets.
- `//small[@class="author"]/text()` goes down to the author's name and returns its text.
- The two string pieces on separate lines are joined by Python into one expression, because adjacent strings are glued together.

**Reading the result.** `['Walter Pike', 'Henrik Sall', 'Tomas Reyna']`: three quotes tagged `work`, by three different authors, in page order.

**Checking.** Count the `work` tags on the page in exercise 9.1's variation: 3. Read the three quotes in the browser and look at their tags.

**Mistakes this exercise provokes.**

- `text()="Work"` with a capital: an empty list. XPath comparisons are exact.
- Leaving out `/text()`: you get the `small` elements themselves, printed as `<Element small at 0x...>`.
- Writing the two strings on separate lines without brackets around them: Python ends the statement at the first line.

**The choice it makes.** `text()="work"` compares each text piece directly inside the `a`; on these tags, which hold one plain word, it is exact. For text that may contain inner tags or spaces, `normalize-space()="work"` or `contains(., "work")` is safer (Chapter 10's trap box).

**Another way to solve it.** Start from the tag and climb back to its quote with `ancestor`:

```python
authors = tree.xpath(
    '//a[@class="tag" and text()="work"]'
    '/ancestor::div[@class="quote"]//small[@class="author"]/text()'
)
```

The same three authors. A condition in brackets reads *quotes that have...*; the `ancestor` path reads *from the tag, up to its quote*. Choose the one that matches how you think about the page.

**A variation to try.** Change the tag to `courage`: `['Tomas Reyna', 'Tomas Reyna']`. The same author twice, because he wrote both `courage` quotes. Then return the text of the quotes instead of the authors: replace the last step with `/span[@class="text"]/text()`.

**If your output differs.**

1. **An empty list**: check the case of `work` and the quotes around it.
2. **Every author of the page**: the condition in brackets is missing its leading dot, so it tests the whole page.
3. **`<Element small ...>`**: add `/text()`.
