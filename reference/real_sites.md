# Public websites used in the book

The *Now try it on a real site* sections use public websites that belong to other people. They can change, move or close after the book is printed. Run `python check_real_sites.py` to see which addresses still answer.

When a site has **changed**, adapt your selectors: open the page, find the new structure in the Elements panel (Chapter 10) and update your code. That is the skill the book teaches.

When a site is **gone**, use the alternative below. The Practice Ground, on your own computer, covers every skill in the book and never changes.

| Site in the book | Chapters | Alternative |
|---|---|---|
| `books.toscrape.com` | 7–13, 23 | `web-scraping.dev/products`; the Practice Ground library |
| `quotes.toscrape.com` (and `/js/`, `/js-delayed/`, `/scroll`, `/login`) | 9–12, 16–18 | Practice Ground quotes (`/quotes/`, `/quotes/js/`) and account (`/account/`) |
| `scrapethissite.com` | 12, 15, 18 | Practice Ground tables (`/tables/`) and shop (`/shop/`) |
| `webscraper.io/test-sites` | 12, 16, 17 | Practice Ground shop (infinite scroll, hidden API) |
| `the-internet.herokuapp.com` | 16, 17 | Practice Ground shop and account; `testpages.eviltester.com` |
| Oxylabs Scraping Sandbox | 16 | Practice Ground shop |
| `realpython.github.io/fake-jobs` | 24 | Practice Ground jobs (`/jobs/`) |
| `httpbin.org` | 8 | Practice Ground Trouble zone (`/trouble/`); `postman-echo.com` |
| JSONPlaceholder | 14 | Practice Ground open API (`/api/`); `dummyjson.com` |
| Open-Meteo, data.gov.uk and the other APIs of Chapter 14 | 14, 26 | The Practice Ground open API; the API's own documentation page for its new address |

Before scraping any alternative, apply the checklist of Chapter 5: read its `robots.txt` and its terms, and keep one request per second with a named User-Agent.
