# Chapter 5 — detailed solutions

These are the solutions printed in the book, word for word: what the question asks, the plan, the code, line by line, reading the result, checking, the mistakes the exercise provokes, the choice it makes, another way to solve it, a variation to try, and what to do if your output differs. Here, each program is followed by its exact output.

Start the Practice Ground first (`python run_site.py`) and run every program from the repository folder, as in the book. Every output below was produced by running the code.

---

## Exercise 5.1 (easy)

> Using `RobotFileParser`, print whether the robot `LearningScraper` may fetch `/quotes/`, `/admin/` and `/private/notes.html` on the Practice Ground. Expected output:

**What the question asks.** Three yes-or-no answers from `robots.txt`: may a robot called `LearningScraper` fetch each of three addresses?

**The plan.** Load `robots.txt` once with `RobotFileParser`, then ask `can_fetch` for each path, with the robot's name and the full address.

```python
from urllib.robotparser import RobotFileParser

robots = RobotFileParser("http://localhost:8000/robots.txt")
robots.read()
for path in ["/quotes/", "/admin/", "/private/notes.html"]:
    print(
        path,
        robots.can_fetch(
            "LearningScraper", "http://localhost:8000" + path
        ),
    )
```

Output:

```text
/quotes/ True
/admin/ False
/private/notes.html False
```

**Line by line.**

- `RobotFileParser(".../robots.txt")` creates a parser for that file; `robots.read()` downloads and reads it.
- The `for` loop takes the three paths in turn.
- `"http://localhost:8000" + path` builds the full address; gluing is safe here because every path starts with `/`.
- `robots.can_fetch("LearningScraper", address)` returns `True` if the rules for that robot allow the address, `False` otherwise.
- `print(path, ...)` prints the path and the answer side by side.

**Reading the result.** `/quotes/` is allowed; `/admin/` and `/private/notes.html` are not. The Practice Ground's `robots.txt` has no group for `LearningScraper`, so the parser applies the group `User-agent: *`, which contains `Disallow: /private/` and `Disallow: /admin/`.

**Checking.** Open `http://localhost:8000/robots.txt` in the browser and read the two `Disallow` lines of the `*` group. `/private/notes.html` is forbidden although the page does not exist: `Disallow: /private/` forbids every address that **starts with** `/private/`.

**Mistakes this exercise provokes.**

- Forgetting `robots.read()`: the parser has no rules yet and answers `False` to everything.
- Testing `/admin` without the final slash: `can_fetch` returns `True`, because `/admin` does not start with `/admin/`. A rule matches the start of the path, character by character.
- Reading `robots.txt` by eye and guessing: the parser applies the rules exactly, including which group applies to which robot.

**The choice it makes.** `can_fetch` answers what `robots.txt` says, not what the law or the terms allow. It is one of the five checks of section 5.5, not all of them.

**Another way to solve it.** Store the answers in a dictionary instead of printing them, so that a scraper can use them later:

```python
allowed = {
    path: robots.can_fetch("LearningScraper", "http://localhost:8000" + path)
    for path in ["/quotes/", "/admin/", "/private/notes.html"]
}
print(allowed)
```

```text
{'/quotes/': True, '/admin/': False, '/private/notes.html': False}
```

**A variation to try.** Ask about `/admin` (no final slash) and predict the answer first. It is `True`: the rule `Disallow: /admin/` only covers addresses starting with `/admin/`. A site owner who wants to block both writes `Disallow: /admin`. Then ask for the robot `SlowBot`: `robots.crawl_delay("SlowBot")` returns `5`, the number of seconds that robot must wait between requests.

**If your output differs.**

1. **`False` for every path**: `robots.read()` is missing, or the Practice Ground is not running.
2. **`True` for `/admin/`**: check the robot's name and the full address you pass.

---

## Exercise 5.2 (easy)

> Print the address of the sitemap announced in `robots.txt`, using the parser's `site_maps()` method, then print how many addresses the sitemap lists (count the `<loc>` tags). Expected output:

**What the question asks.** Follow the chain a crawler follows: from `robots.txt` to the sitemap it announces, and from the sitemap to the number of pages it lists.

**The plan.** Read `robots.txt`; take the sitemap address from `site_maps()`; download the sitemap; count its `<loc>` tags, one per address.

```python
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

robots = RobotFileParser("http://localhost:8000/robots.txt")
robots.read()
sitemap_url = robots.site_maps()[0]
print(sitemap_url)
xml = requests.get(sitemap_url, timeout=10).text
soup = BeautifulSoup(xml, "xml")
print(len(soup.find_all("loc")), "addresses")
```

Output:

```text
http://localhost:8000/sitemap.xml
10 addresses
```

**Line by line.**

- `robots.site_maps()` returns the list of addresses given on `Sitemap:` lines; `[0]` takes the first.
- `requests.get(sitemap_url, timeout=10).text` downloads the sitemap, an XML file.
- `BeautifulSoup(xml, "xml")` parses it **as XML**. XML is stricter than HTML and is read by a different parser (from the `lxml` package, already installed); with `"html.parser"`, BeautifulSoup prints a long `XMLParsedAsHTMLWarning`.
- `soup.find_all("loc")` returns every `<loc>` element; `len(...)` counts them.

**Reading the result.** The sitemap is at `http://localhost:8000/sitemap.xml` and lists 10 addresses: the home page and the main sections of the Practice Ground.

**Checking.** Open the sitemap in the browser: it is a list of `<url>` blocks, each with one `<loc>`. Count them.

**Mistakes this exercise provokes.**

- `robots.site_maps()` without `[0]`: you print a list, and `requests.get` on a list fails.
- Parsing with `"html.parser"`: the count is right, but a warning fills the screen. Use `"xml"` for XML documents.
- Counting `<url>` and `<loc>` together: 20, every address twice.

**The choice it makes.** `site_maps()` returns a list because a `robots.txt` can announce several sitemaps; this one announces one. A sitemap is the owner's own list of pages: on a real site, it is often the best starting point for a crawler, because it lists pages the owner wants found.

**Another way to solve it.** Without BeautifulSoup, with `lxml` directly. A sitemap declares a *namespace*, so the search must name it:

```python
from lxml import etree

root = etree.fromstring(xml.encode())
ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
print(len(root.findall(".//s:loc", ns)), "addresses")
```

It prints `10 addresses`. Without `ns`, `findall(".//loc")` finds nothing: that is the most common surprise with sitemaps.

**A variation to try.** Print the first three addresses instead of counting them: `[loc.text for loc in soup.find_all("loc")][:3]` gives the home page, `/library/` and `/quotes/`. Then check each against `robots.txt` with `robots.can_fetch(...)` before visiting it: a sitemap can list pages that `robots.txt` forbids to some robots.

**If your output differs.**

1. **`IndexError: list index out of range`** on `site_maps()[0]`: `site_maps()` returned `None`, meaning no `Sitemap:` line was read; check `robots.read()`.
2. **A long `XMLParsedAsHTMLWarning`**: you parsed with `"html.parser"`; the count is still right, but use `"xml"`.
3. **`bs4.FeatureNotFound`**, with the message *Couldn't find a tree builder with the features you requested: xml*: `lxml` is not installed in your environment; run `pip install -r requirements.txt` again.

---

## Exercise 5.3 (medium)

> A robot called *BadBot* wants to scrape the library. Print what `robots.txt` answers for it, then explain in a comment of your program why. Expected output:

**What the question asks.** What `robots.txt` answers to a robot it names explicitly, and why, written as a comment so that the reason stays in the program.

**The plan.** Ask `can_fetch` with the name `BadBot` and an address of the library; read the `BadBot` group in the file to explain the answer.

```python
from urllib.robotparser import RobotFileParser

robots = RobotFileParser("http://localhost:8000/robots.txt")
robots.read()
print(robots.can_fetch("BadBot", "http://localhost:8000/library/"))
# The group "User-agent: BadBot" contains "Disallow: /",
# which forbids every address of the site to this robot.
```

Output:

```text
False
```

**Line by line.**

- `robots.can_fetch("BadBot", ".../library/")` looks for a group whose `User-agent` matches `BadBot`, and finds one.
- That group has a single rule, `Disallow: /`. Every path starts with `/`, so every address is forbidden.
- The comment lines, starting with `#`, are ignored by Python; they record the reason for the next reader.

**Reading the result.** `False`. Not only for the library: for every address of the site, including the home page.

**Checking.** Open `robots.txt` and find the lines `User-agent: BadBot` and `Disallow: /`. Then ask for the same address with the robot `LearningScraper`: `True`, because that robot falls under the `*` group, which does not forbid `/library/`.

**Mistakes this exercise provokes.**

- Checking with `can_fetch("*", ...)` gives `True`, and BadBot happily scrapes a site that banned it by name. The check must use the robot's real name.
- Thinking that a named group adds to the `*` group: a robot follows **only** the most specific group that matches its name, not both.
- Changing the robot's name to get round the ban: technically easy, and exactly what the owner asked you not to do.

**The choice it makes.** A site can ban one robot while welcoming others. Your scraper's name, sent in the `User-Agent` header, is how the site recognises you; use an honest name and check the rules for that name.

**Another way to solve it.** The parser matches names without regard to case, and on the first word of the name, so these all return `False`:

```python
for name in ["BadBot", "badbot", "BadBot/2.0"]:
    print(name, robots.can_fetch(name, "http://localhost:8000/library/"))
```

**A variation to try.** Ask for `robots.txt` itself: `robots.can_fetch("BadBot", "http://localhost:8000/robots.txt")` returns `True`. Reading `robots.txt` is always allowed, otherwise no robot could learn the rules.

**If your output differs.**

1. **`True`**: you asked with another name, or for the `*` group.
2. **`False` for every robot**: `robots.read()` failed; is the Practice Ground running?

---

## Exercise 5.4 (harder)

> Change `polite_get` so it also refuses to run when the response status is 429, 403 or 401, printing `Stopping: status 403` (for example) and returning `None`. Test it on `/library/` and `/trouble/status/403`. Expected output:

**What the question asks.** Make `polite_get` stop by itself when the site says *stop*: on 401 (you must log in), 403 (forbidden) and 429 (too many requests). It must print the reason and return `None`.

**The plan.** After the request, test the status code against the three refusals; if it matches, print and return `None`; otherwise return the response as before.

```python
import time
from urllib.robotparser import RobotFileParser

import requests

AGENT = "LearningScraper/1.0 (+mailto:reader@example.com)"
BASE = "http://localhost:8000"
robots = RobotFileParser(BASE + "/robots.txt")
robots.read()
delay = robots.crawl_delay(AGENT) or 0.2   # 0.2 s: the site's terms


def polite_get(url):
    if not robots.can_fetch(AGENT, url):
        print("Not allowed by robots.txt:", url)
        return None
    time.sleep(delay)
    response = requests.get(url, headers={"User-Agent": AGENT}, timeout=10)
    if response.status_code in (401, 403, 429):
        print("Stopping: status", response.status_code)
        return None
    return response


for path in ["/library/", "/trouble/status/403"]:
    r = polite_get(BASE + path)
    if r is not None:
        print(r.status_code, path)
```

Output:

```text
200 /library/
Stopping: status 403
```

**Line by line.**

- `AGENT` names the robot honestly, with a way to contact you.
- `robots.crawl_delay(AGENT) or 0.2` uses the delay `robots.txt` gives this robot, or 0.2 seconds, the site's terms, when it gives none (`None or 0.2` is `0.2`).
- In `polite_get`, the first check refuses addresses forbidden by `robots.txt`.
- `time.sleep(delay)` waits before every request.
- `requests.get(..., headers={"User-Agent": AGENT}, timeout=10)` sends the name and gives up after 10 seconds without an answer.
- `if response.status_code in (401, 403, 429):` tests the code against the three values at once.
- `return None` hands back *nothing*, so the caller knows to stop.
- In the test loop, `if r is not None:` prints only the responses that came back.

**Reading the result.** `/library/` comes back with 200. `/trouble/status/403` is refused: `Stopping: status 403`, and nothing else is printed for it.

**Checking.** Add `/trouble/status/429` and `/trouble/status/401` to the list: each prints `Stopping: status ...`. Add `/admin/`: it prints `Not allowed by robots.txt`, before any request is sent.

**Mistakes this exercise provokes.**

- Testing with `==` against a tuple, `status_code == (401, 403, 429)`: always `False`. Use `in`.
- Checking `response.ok` only: it also stops on 404 and 500, which are not refusals but missing pages and server errors, handled differently.
- Forgetting `if r is not None:` in the caller: `r.status_code` on `None` stops with `AttributeError`.

**The choice it makes.** Here 429 stops the scraper. In Chapter 20 you will make it wait and try again instead, using the `Retry-After` header the site sends. A 401 or 403, on the other hand, is a refusal: never retry it.

**Another way to solve it.** Raise an exception instead of returning `None`, so that a refusal cannot be ignored by mistake:

```python
class Refused(Exception):
    pass


def polite_get(url):
    ...
    if response.status_code in (401, 403, 429):
        raise Refused(f"status {response.status_code} for {url}")
    return response
```

The caller then writes `try: ... except Refused as e: print("Stopping:", e)`. Returning `None` is simpler; raising is safer in long programs. Chapter 20's `PoliteClient` raises, for that reason.

**A variation to try.** Count the refusals: keep a variable `refused = 0`, add 1 each time `polite_get` returns `None`, and stop the whole loop with `break` after three refusals. A scraper that keeps knocking on a door that says no gets banned.

**If your output differs.**

1. **`403 /trouble/status/403`**: the status test is missing or after the `return`.
2. **`Not allowed by robots.txt` for `/library/`**: check `AGENT` and the address.
3. **The program waits a long time**: `crawl_delay` returned a large value; print `delay`.

---

## Exercise 5.5 (thinking, no code)

> For each project, say which of the five checklist questions blocks it, if any: (a) collecting the email addresses of every author on a public forum to send them a newsletter; (b) downloading the daily list of eligible assets that a central bank publishes as a file, for your own analysis; (c) copying every review of a shop to publish them on your own website.

**What the question asks.** No code: apply the five questions of the checklist (section 5.5) to three projects, and say which question, if any, stops each one.

**The plan.** Go through the questions in order for each project: (1) is there an official route? (2) what do the terms say? (3) what does `robots.txt` say? (4) is there personal data? (5) what will you do with the data? Stop at the first question that blocks.

**Answers.**

- **(a) Email addresses from a forum, for a newsletter.** Blocked by question 4. Email addresses are personal data, even when public; collecting them is processing them, and sending a newsletter needs the people's consent. Question 5 blocks it too: you would use the data for something the people never agreed to.
- **(b) A central bank's daily list of eligible assets, published as a file, for your own analysis.** Allowed, by question 1: an official file published for download **is** the official route, so you download it rather than scrape a page. Before you publish anything built from it, read its terms of reuse (question 5).
- **(c) Copying every review of a shop to publish them on your own website.** Blocked by questions 2 and 5. Reviews are texts protected by copyright, written by people (so also personal data, question 4), and shops' terms forbid this reuse. Republishing them is the use that turns a technical possibility into an infringement.

**Checking your answers.** For each project, ask: who would be harmed or surprised if they saw what you do? The forum members (a), nobody (b), the reviewers and the shop (c).

**Mistakes this exercise provokes.**

- *"It is public, so I may take it."* Public is not the same as free to reuse: personal data and copyright still apply to public pages.
- *"robots.txt allows it, so it is legal."* `robots.txt` answers question 3 only.
- Treating (b) as scraping: when a file is offered for download, download the file.

**The choice it makes.** The checklist is ordered so that the cheapest question comes first: an official route ends the analysis in one step. This is good practice, not legal advice: for a commercial project or any personal data, ask a lawyer.

**A variation to try.** Apply the checklist to two more projects:

- **(d)** Recording the price of ten products on a shop every morning to see how they change. Question 3 decides how (respect `robots.txt` and the delay); question 2 decides whether (search the terms for *automated*). Prices are facts, not personal data. This is Chapter 25's project, done on the Practice Ground.
- **(e)** Collecting the job titles and salaries of a public job board to study the market. Usually allowed for personal analysis if the terms do not forbid it; remove any recruiter's name (question 4). This is Chapter 24's project.

**If your answers differ.** Compare your reasoning, not only your verdict: two people can reach the same answer for different reasons, and the reason is what protects you on the next project.
