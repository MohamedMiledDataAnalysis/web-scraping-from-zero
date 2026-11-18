# Chapter 6 — detailed solutions

These are the long versions of the solutions printed in the book. Each has the same parts as the book, with more detail, plus parts the book has no room for: another way to solve the exercise, a variation to try, and what to do if your output differs.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 6.1 (easy)

> Print the number of results of the job board for the site date, then for 15 March 2027. The number is in the paragraph with the class `result-count`. Expected output:

**What the question asks.** The same number read twice: the count of job offers on the site date (1 March 2027), and on 15 March 2027, which the job board shows when the address carries `?day=2027-03-15`.

**The plan.** Loop over two values of `day`: an empty one (no parameter) and `2027-03-15`. Build the address, download, read the paragraph `.result-count`.

```python
import requests
from bs4 import BeautifulSoup

for day in ["", "2027-03-15"]:
    url = "http://localhost:8000/jobs/"
    if day:
        url += "?day=" + day
    soup = BeautifulSoup(requests.get(url, timeout=10).text, "html.parser")
    print(day or "site date", "->", soup.select_one(".result-count").text)
```

Output:

```text
site date -> 50 jobs
2027-03-15 -> 55 jobs
```

**Line by line.**

- `for day in ["", "2027-03-15"]:` runs the body twice; the empty string stands for *no day given*.
- `url = "http://localhost:8000/jobs/"` starts from the bare address on each turn.
- `if day:` is true only for a non-empty string; then `url += "?day=" + day` adds the parameter.
- `soup.select_one(".result-count").text` reads the paragraph with the class `result-count`, such as `50 jobs`.
- `day or "site date"` gives `day` when it is not empty, and `"site date"` otherwise: an empty string counts as false in Python.

**Reading the result.** 50 offers on the site date, 55 on 15 March. The board changes with the date, like a real one: offers appear and expire.

**Checking.** Open both addresses in the browser; each page shows the same number at the top of the list.

**Mistakes this exercise provokes.**

- Building the address outside the loop and adding `?day=` to it: on the second turn the address already holds a parameter, and the next one would add a second `?`.
- A date in another format, such as `?day=15/03/2027`: the site answers with status 400 (bad request) and no `.result-count`, so `select_one` returns `None` and `.text` stops with `AttributeError`.
- Forgetting `.text`: you print the whole tag, `<p class="result-count">50 jobs</p>`.

**The choice it makes.** Gluing `"?day=" + day` is fine for one simple value. With several parameters or special characters, let `requests` build the query: `requests.get(url, params={"day": day})`, which Chapter 8 introduces.

### Another way to solve it

Let `requests` add the parameter, and check the address it built:

```python
r = requests.get("http://localhost:8000/jobs/", params={"day": "2027-03-15"})
print(r.url)
```

```text
http://localhost:8000/jobs/?day=2027-03-15
```

With `params`, an empty value is easy to leave out: build the dictionary only when `day` is not empty.

### A variation to try

Print the count for four dates and watch the board move: 1 March 50, 8 March 59, 31 March 47, and 1 February 55. Chapter 22 records this every day and compares days.

### If your output differs

1. **`AttributeError: 'NoneType' object has no attribute 'text'`**: the page has no `.result-count`; print `r.status_code`. 400 means the date format is wrong: use `YYYY-MM-DD`.
2. **The same number twice**: the parameter was not added; print `url` inside the loop.
3. **Another number for the site date**: the site was started with `--live` or `--date`; restart it with `python run_site.py`.

---

## Exercise 6.2 (medium)

> The Files section lists the files you can download in a table with the id `file-list`. Print the name and size of each file. Expected output:

**What the question asks.** Read a table row by row: for each file listed in the table `#file-list`, its name and its size, printed in two aligned columns.

**The plan.** Select the rows of the table's body (not the header), take the text of each row's cells, and print them with an f-string that sets the width of each column.

```python
import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/files/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
for row in soup.select("#file-list tbody tr"):
    name, size = [td.text for td in row.find_all("td")]
    print(f"{name:<30} {int(size):>7,} bytes")
```

Output:

```text
arrears_report_2026.pdf          2,189 bytes
bank_capital_eu.csv              1,707 bytes
cover_pool_synthetic.xlsx        5,251 bytes
eligible_assets.txt              4,692 bytes
market_report_q4_2026.xlsx       6,668 bytes
monthly_sales.csv                1,297 bytes
```

**Line by line.**

- `#file-list` selects the element whose `id` is `file-list`; `tbody tr` then takes the rows inside its body, without the header row in `thead`.
- `row.find_all("td")` returns the cells of one row; `[td.text for td in ...]` takes their texts.
- `name, size = [...]` puts the two texts into two variables at once (*unpacking*). It works because every body row has exactly two cells.
- `int(size)` turns the size text into a number.
- In the f-string, `{name:<30}` writes the name left-aligned in 30 characters; `{int(size):>7,}` writes the number right-aligned in 7 characters, with a thousands comma.

**Reading the result.** Six files, sizes from 1,297 to 6,668 bytes, in a neat table. The alignment comes from the format codes, not from the page.

**Checking.** Open `http://localhost:8000/files/` in the browser: the same six names, in the same order. Add the sizes: 21,804 bytes in total.

**Mistakes this exercise provokes.**

- `soup.select("#file-list tr")` also returns the header row, whose cells are `th`, not `td`: `find_all("td")` gives an empty list for it, and `name, size = []` stops with `ValueError: not enough values to unpack (expected 2, got 0)`.
- `{size:>7,}` without `int()`: `ValueError: Cannot specify ',' with 's'`, because the comma format needs a number.
- `#file_list` with an underscore: no match, nothing printed.

**The choice it makes.** Chapters 9 and 10 explain `select` in full; copy it for now. Chapter 7 reads the same table in one line with pandas, which is the better tool for whole tables; the loop shows what pandas does for you.

### Another way to solve it

With pandas, as in Chapter 7:

```python
from io import StringIO

import pandas as pd

table = pd.read_html(StringIO(html), attrs={"id": "file-list"})[0]
print(table)
```

```text
                         File  Size (bytes)
0     arrears_report_2026.pdf          2189
1         bank_capital_eu.csv          1707
2   cover_pool_synthetic.xlsx          5251
3         eligible_assets.txt          4692
4  market_report_q4_2026.xlsx          6668
5           monthly_sales.csv          1297
```

pandas uses the header row for the column names and converts the sizes to numbers itself.

### A variation to try

Print the total size of the six files. Keep the sizes in a list inside the loop, then `print(sum(sizes))`: 21804. Then print the largest file's name: keep pairs `(size, name)` and use `max(pairs)`.

### If your output differs

1. **`ValueError: not enough values to unpack`**: your selector includes the header row; add `tbody`.
2. **Nothing printed**: print `soup.select_one("#file-list")` to check the id.
3. **The columns are not aligned**: a name is longer than 30 characters; raise the width.

---

## Exercise 6.3 (medium)

> Print the first three links of the Trouble zone list (`ul.trouble-list`) with their text: the address, two spaces, then the explanation after the colon. Expected output:

**What the question asks.** From a list of links followed by explanations, the first three items, each printed as the address, two spaces, and the explanation that follows the colon.

**The plan.** Select the `li` items of `ul.trouble-list` and keep three. In each, read the link's `href`, cut the item's text at the first colon, and keep the part after it.

```python
import requests
from bs4 import BeautifulSoup

html = requests.get("http://localhost:8000/trouble/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
for item in soup.select("ul.trouble-list li")[:3]:
    link = item.a["href"]
    explanation = item.get_text().split(":", 1)[1].strip()
    print(link, "", explanation)
```

Output:

```text
/trouble/status/404  any status code you put in the address
/trouble/old-page  a permanent redirect (301)
/trouble/slow?seconds=3  a slow page
```

**Line by line.**

- `soup.select("ul.trouble-list li")[:3]` returns the items of that list and keeps the first three.
- `item.a["href"]` reads the address of the link inside the item.
- `item.get_text()` returns all the text of the item, link included: `/trouble/status/404: any status code you put in the address`.
- `.split(":", 1)` cuts at the **first** colon only and returns two pieces; `[1]` keeps the second.
- `.strip()` removes the space left after the colon.
- `print(link, "", explanation)` prints three items separated by spaces; the empty string in the middle gives two spaces in a row.

**Reading the result.** Three lines, each an address and what that address of the Trouble zone does: any status code, a redirect, a slow page. You will use these pages in Chapters 4, 8 and 20.

**Checking.** Open `http://localhost:8000/trouble/`: the list has eight items, and the first three match. `print(len(soup.select("ul.trouble-list li")))` prints 8.

**Mistakes this exercise provokes.**

- `split(":")` without the `1`: it cuts at **every** colon. It works on these items, but an explanation or an address containing a colon (such as `http://`) would be cut in pieces, and `[1]` would keep only part of the text.
- `item.text` vs `item.a.text`: the link's text is the address only, without the explanation.
- Forgetting `.strip()`: the explanation starts with a space.

**The choice it makes.** Cutting the text at a colon depends on how the page writes its items. If the page put the explanation in its own tag, selecting that tag would be more robust; here, the colon is the only separator the page gives.

### Another way to solve it

The explanation is the text that follows the link inside the item. BeautifulSoup reaches it with `next_sibling`, the node right after the `<a>`:

```python
for item in soup.select("ul.trouble-list li")[:3]:
    print(item.a["href"], item.a.next_sibling)
```

```text
/trouble/status/404 : any status code you put in the address
/trouble/old-page : a permanent redirect (301)
/trouble/slow?seconds=3 : a slow page
```

The colon is still there, because it is part of that text; remove it with `.removeprefix(": ")`. This version depends on the exact tree; the `split` version only on the visible text.

### A variation to try

Print the addresses of all eight items, without explanations, as a Python list: `[li.a["href"] for li in soup.select("ul.trouble-list li")]`. Among them, `/trouble/agent` returns in Chapter 8, and `/trouble/limited` and `/trouble/flaky` in Chapter 20.

### If your output differs

1. **`IndexError: list index out of range`**: an item has no colon; print `item.get_text()`.
2. **Only part of the explanation**: you split without the `1`.
3. **One space between the address and the explanation**: the `""` in `print` is missing.
