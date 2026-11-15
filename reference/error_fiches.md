# Error fiches

Each fiche starts from **what you see**, the last line of the error or the symptom. It names the scraping step that failed (fetch, parse, extract, save), lists the causes from the most frequent, and gives the fix. Then the loop: *Is it solved?* If not, *tell me what you see*: the fiche sends you to the next check.

How to use them: copy the **last line** of your error, find it in the list below, and follow the fiche from the top.

| What you see | Fiche |
|---|---|
| `ConnectionError ... Connection refused` | 1 |
| `ModuleNotFoundError: No module named ...` | 2 |
| `403 Forbidden` | 3 |
| `404 Not Found` | 4 |
| `429 Too Many Requests` | 5 |
| `Timeout`, `ReadTimeout` | 6 |
| `CERTIFICATE_VERIFY_FAILED` | 7 |
| `'NoneType' object has no attribute 'text'` | 8 |
| empty results, `[]`, zero items, no error | 9 |
| `IndexError: list index out of range` | 10 |
| `Ã©`, `â‚¬`, `\x00`, `UnicodeDecodeError` | 11 |
| My numbers are wrong or read as text | 12 |
| `KeyError` | 13 |
| `JSONDecodeError` | 14 |
| Playwright or Selenium `TimeoutError` | 15 |
| Sent back to the login page | 16 |
| Scrapy finishes with 0 items | 17 |

## Fiche 1. ConnectionError: Connection refused

**Step:** fetch. Nothing answered at that address.

1. **The site is not running** (Practice Ground). Look at its terminal: if you see the prompt, start it with `python run_site.py`.
2. **Wrong port or host**: `localhost:8000` and `localhost:8001` are different doors. Compare the address in your code with the one in your browser.
3. **A real site**: your internet connection is down, or the address is misspelt. Open it in your browser.

**Is it solved?** Run `python chapters/ch06/examples/health_check.py`: every line starts with 200. Still refused? Tell me what you see: if the browser opens the page and Python does not, check for a proxy at your workplace, and try from home or from Codespaces.

## Fiche 2. ModuleNotFoundError: No module named ...

**Step:** before everything. Python cannot find a package.

1. **The virtual environment is not active** in this terminal: no `(.venv)` at the start of the prompt. Activate it (Chapter 0, section 0.6).
2. **VS Code uses another Python**: Ctrl+Shift+P, *Python: Select Interpreter*, choose `.venv`.
3. **The package was never installed**: `python -m pip install -r requirements.txt`.
4. **A typing mistake in the import**: `import bs4` (not `beautifulsoup4`), `from bs4 import BeautifulSoup`.
5. **Your own module**: run the program from the repository's folder, or add its folder with `sys.path.insert`.

**Is it solved?** `python check_setup.py` lists every package with a version. Still missing? Tell me what you see: `python -c "import sys; print(sys.executable)"` prints which Python runs; it must be inside `.venv`.

## Fiche 3. 403 Forbidden

**Step:** fetch. The site refused you.

1. **No User-Agent, or the default `python-requests`**: name your scraper with a contact (Chapter 8). The Practice Ground's `/trouble/agent` shows this case.
2. **You need to log in**: Chapter 18, and only on an account you are allowed to use.
3. **The site blocks robots**: its terms or robots.txt say no. **Stop.** Do not disguise your scraper as a browser.
4. **Too many requests earlier**: some sites answer 403 instead of 429. Stop, wait, slow down.

**Is it solved?** The status is 200 with your named User-Agent. Still 403 with a correct User-Agent and no login needed? The site does not want robots: use an official route (API, download, a request to the owner).

## Fiche 4. 404 Not Found

**Step:** fetch. The page does not exist.

1. **The address is built wrongly**: print it. Missing `.html`, a doubled `/`, a relative link joined with `+` instead of `urljoin`.
2. **You went past the last page**: stop on the *next* link (Chapter 12), not on a fixed number.
3. **The page was removed**: normal on real sites. Record it and skip it; never retry a 404.

**Is it solved?** The same address opens in your browser. Still 404 in Python but not in the browser? Tell me what you see: compare `response.url` (after redirects) with the browser's address bar.

## Fiche 5. 429 Too Many Requests

**Step:** fetch. You go too fast.

1. Read `Retry-After` and wait that long (Chapter 20).
2. Then **slow down for the rest of the run**: increase your delay.
3. Check that you use one `PoliteClient` or one session with a delay, not several programs at once.

**Is it solved?** A full run with no 429. Still 429 at your new speed? The limit may be per hour or per day: read the API's documentation or the site's terms, and spread the work over time.

## Fiche 6. Timeout, ReadTimeout

**Step:** fetch. The site did not answer in time.

1. **The site is slow** right now: retry with backoff (Chapter 20).
2. **Your timeout is too short** for this page: 10 to 30 seconds for real sites.
3. **The site is overloaded** (perhaps by scrapers): slow down, try later.

**Is it solved?** Most pages succeed after one retry. Every page times out? Tell me what you see: open the page in your browser; if it is slow there too, the site has a problem; come back later.

## Fiche 7. SSL: CERTIFICATE_VERIFY_FAILED

**Step:** fetch, on `https` addresses.

1. **macOS**: run *Install Certificates.command* in the Python folder (Chapter 0).
2. **A company network** that inspects encrypted traffic: work from home or Codespaces, or ask your IT team for the certificate.
3. **The site's certificate has really expired**: wait, or contact the site.

Never "fix" it with `verify=False` in a scraper you keep: it removes the protection that tells you you are talking to the real site.

## Fiche 8. AttributeError: 'NoneType' object has no attribute 'text'

**Step:** extract. `find` or `select_one` found nothing, returned `None`, and you called `.text` on it.

1. **The element is missing on this card** (a product without price): check for `None` first (Chapter 9, `text_or_none`).
2. **The selector is wrong**: test it in the Elements panel with Ctrl+F (Chapter 10). A missing dot (`price` instead of `.price`) is the classic one.
3. **The page is not the one you think**: an error page, a login page, a cookie banner. Print `response.status_code` and `soup.title`.
4. **The element is added by JavaScript**: go to fiche 9.

**Is it solved?** The program runs through every card, and missing values appear as `None` in your table. Still failing on every card? Print `card.prettify()[:500]` for the first card and compare it with your selector.

## Fiche 9. Empty results, no error

**Step:** fetch or extract. The most dangerous fiche: nothing tells you anything is wrong.

1. **The data comes from JavaScript**: Ctrl+U then Ctrl+F for a value you see on screen. Not in the source? Look in the Network panel, filter *Fetch/XHR*, for a hidden API (Chapter 15), or use Playwright (Chapter 16).
2. **The selector does not match**: count first, `print(len(soup.select(...)))`; test in the Elements panel.
3. **You received a different page**: consent page, login page, error page with status 200. Save the HTML and open it in your browser: `Path("debug.html").write_text(response.text)`.
4. **robots.txt forbids it** (Scrapy, `PoliteClient`): read the log.

**Is it solved?** Your checks (Chapter 20) pass: the count matches what the site announces. Still empty? Tell me what you see: compare the saved `debug.html` with what your browser shows; the difference is your answer.

## Fiche 10. IndexError: list index out of range

**Step:** extract. You took item `[n]` of a list that is shorter, usually empty.

1. **The selector found nothing**: fiche 9.
2. **`split` gave fewer pieces than expected**: print the text with `repr()`; the separator may be a different character (an en dash `–`, not a hyphen `-`).
3. **A table row has fewer cells**: header rows have `th`, not `td`.

**Is it solved?** Print `len()` before every `[n]`. Use `[0]` only after checking the list is not empty, or `select_one` instead of `select(...)[0]`.

## Fiche 11. Garbled characters, UnicodeDecodeError

**Step:** fetch or save. Bytes read with the wrong encoding.

1. **`Ã©` for `é`, `Â£` for `£`**: UTF-8 read as ISO-8859-1 or Windows-1252. Set `response.encoding = "utf-8"` before `.text` (Chapter 8).
2. **`\x00` between letters**: UTF-16. Use `encoding="utf-16"` (Chapter 19).
3. **`UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff`**: a UTF-16 file, or a binary file (Excel, PDF) read as text. Look at the first bytes.
4. **Excel shows rubbish in your CSV**: save with `encoding="utf-8-sig"`; Excel then recognises UTF-8.

**Is it solved?** Accents and currency signs look right in the file. Still wrong? Tell me what you see: `open(path, "rb").read(20)` shows the raw bytes; compare with the table of section 19.3.

## Fiche 12. My numbers are wrong or read as text

**Step:** extract or save.

1. **`ValueError: could not convert string to float: '£1,049.00'`**: remove the currency sign and the thousands separator first, or use the regular expression of Chapter 13.
2. **`14,63` read as text or as 1463**: decimal comma. `pd.read_csv(..., sep=";", decimal=",", thousands=".")`.
3. **A column is `str` after `read_html` or `read_csv`**: one value is not a number (`n/a`, `-`, a footnote mark). Find it: `df[pd.to_numeric(df[col], errors="coerce").isna()]`.
4. **Totals counted twice**: a *Total* row was kept (Chapter 19).
5. **`NaN` where a formula was**: Excel formulas without saved values; recompute them.

**Is it solved?** `df.dtypes` shows numbers, and a total you compute by hand matches.

## Fiche 13. KeyError

**Step:** extract.

1. **A dictionary key is missing**: use `.get("key")` when the field can be missing (Chapter 3).
2. **An attribute is missing**: `tag.get("href")` instead of `tag["href"]`.
3. **A DataFrame column name is different**: print `list(df.columns)` and copy the name; watch for spaces and capitals.
4. **An API answer has another shape**: print `json.dumps(data, indent=2)[:1000]`; the key may be nested deeper, or the answer is an error.

## Fiche 14. JSONDecodeError

**Step:** fetch. You called `.json()` on something that is not JSON.

1. **The API returned an error page in HTML**: print `r.status_code` and `r.text[:300]`.
2. **A hidden API needs a header**: `Accept: application/json` or others copied from the Network panel (Chapter 15).
3. **The JSON is inside a script**: extract it with a regular expression first (Chapter 11).

**Is it solved?** `r.headers["Content-Type"]` says `application/json`, and `.json()` works.

## Fiche 15. Playwright or Selenium TimeoutError

**Step:** fetch or extract, in a browser.

1. **The selector is wrong**: test it in the Elements panel.
2. **Something covers the page**: cookie banner, pop-up, login wall. Take a screenshot at the moment of the error (Chapter 16) and look at it.
3. **You wait for the wrong thing**: an old element still present, a count that never changes. Wait for a sign of the new state (Chapters 16 and 17).
4. **The element is in a frame**: Playwright `page.frame_locator("iframe")`, Selenium `driver.switch_to.frame(...)`.

**Is it solved?** Run with a visible browser (`headless=False, slow_mo=500`) and watch where it stops.

## Fiche 16. Sent back to the login page

**Step:** fetch, after a login.

1. **You used `requests.get` instead of `session.get`**: only the session carries the cookie (Chapter 18).
2. **The CSRF token was missing or from another session**: load the form and post it in the same session.
3. **The field names are wrong**: copy them from the form's `name` attributes or the Network panel's *Payload*.
4. **The session expired**: log in again at the start of each run.
5. **The site asks for a captcha or a second verification**: stop. That is a no to robots.

**Is it solved?** A members-only element (`#user-name`) is on the page.

## Fiche 17. Scrapy finishes with 0 items

**Step:** any. Read Scrapy's log with `LOG_LEVEL = "INFO"`.

1. **`Forbidden by robots.txt`**: the start address is disallowed for your User-Agent.
2. **`Connection refused`**: fiche 1.
3. **`Crawled (200)` but no items**: your selectors do not match; test them in `scrapy shell "URL"`, Scrapy's interactive console.
4. **`Filtered duplicate request`**: all your requests point to addresses already visited.
5. **Your pipeline drops everything**: look for `Dropped:` lines.

**Is it solved?** The final statistics show `item_scraped_count` with the number you expect.
