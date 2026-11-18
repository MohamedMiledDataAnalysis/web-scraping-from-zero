# I Finally Understand Web Scraping — companion repository

Code, data and the **Practice Ground** website for the book
*I Finally Understand Web Scraping: Collect Data from Websites with Python, Step by Step*
by Mohamed Miled.

Every output printed in the book was produced by running the code in this
repository against the Practice Ground. Run the same code and you get the same output.

## Start in five minutes

1. Install Python 3.11 or later (the book uses 3.13) and download this repository
   (green **Code** button, **Download ZIP**, unzip to a short path such as `C:\scraping` or `~/scraping`).
2. In a terminal, inside the folder:

   ```
   python -m venv .venv
   .venv\Scripts\Activate.ps1          (Windows)   or   source .venv/bin/activate   (macOS, Linux)
   python -m pip install -r requirements.txt
   python -m playwright install chromium
   ```

3. Start the Practice Ground in its own terminal: `python run_site.py`, then open <http://localhost:8000>.
4. In another terminal: `python check_setup.py`. The last line must be **All set: you are ready for Chapter 1**.

No administrator rights? Click **Code**, **Codespaces**, **Create codespace on main**:
everything installs by itself in your browser (see `SETUP.md`).

Chapter 0 of the book walks through every step with what you should see and the fix for every error.

## What is inside

| Folder or file | Content |
|---|---|
| `run_site.py` | starts the Practice Ground (`--live`, `--date 2027-03-15`, `--port 8001`) |
| `site/` | the website (Flask): `app.py`, templates, `data/` (books, quotes, products, jobs, prices, stations) and `files/` (CSV, Excel, UTF-16, PDF) |
| `site/generate_data.py`, `site/generate_files.py` | rebuild the data from a fixed seed |
| `check_setup.py` | the setup check of Chapter 0 |
| `check_real_sites.py` | checks that the public websites of the *Now try it* sections still answer |
| `run_mailbox.py` | the test mailbox of Chapter 22 (emails never leave your computer) |
| `toolkit/` | `PoliteClient` (Chapter 20) and the test mailbox |
| `chapters/chNN/examples/` | every program printed in chapter NN |
| `chapters/chNN/exercises/` | starter files for the exercises |
| `chapters/chNN/solutions/` | full solutions, and `SOLUTIONS.md`: the step-by-step solutions printed in the book, word for word, with the exact output of each program |
| `chapters/chNN/expected/` | the exact output of every program, as printed in the book |
| `chapters/ch23` to `ch26` | the four projects |
| `chapters/ch26/PLAN_TEMPLATE.md` | the plan template for your own project |
| `reference/` | error sheets, cheat sheets, the legal checklist, the glossary, and `real_sites.md` (alternatives if a public site changes or closes) |
| `tests/run_all.py` | runs the programs and compares them with `expected/` |
| `output/` | where the programs write their results (empty in the repository) |

## Chapters

| Part | Chapters |
|---|---|
| 0 | Setting up your computer |
| 1 Foundations | 1 Your toolkit · 2 Python I · 3 Python II · 4 How the web works · 5 Legally and ethically · 6 Your practice ground |
| 2 Static pages | 7 Which method? read_html · 8 requests · 9 BeautifulSoup · 10 CSS selectors and XPath · 11 Structures and JSON-LD · 12 Many pages · 13 Cleaning and saving |
| 3 Dynamic and protected sites | 14 Official APIs · 15 Hidden APIs · 16 Playwright · 17 Selenium · 18 Forms and logins · 19 Files and PDF tables · 20 Robust and polite scrapers |
| 4 Scaling and automating | 21 Scrapy · 22 Scheduling, history and email alerts |
| 5 Projects | 23 Book catalogue, four methods · 24 Job tracker · 25 Price monitor · 26 Capstone |
| 6 Reference | Error sheets · cheat sheets · legal checklist · glossary |

Run every program **from this folder** (the repository's root), for example
`python chapters/ch09/examples/find.py`, with the Practice Ground running.

## Checking that everything works

```
python run_site.py          (terminal 1)
python tests/run_all.py     (terminal 2; add --all to include the long crawls)
```

## Data and licences

- **Code**: MIT licence (see `LICENSE`).
- **Practice Ground data**: invented by `site/generate_data.py` and `site/generate_files.py`
  with a fixed seed. Every book, author, quote, product, job, bank, price and weather figure is invented.
  Free to reuse.
- **Planet figures** (`/tables/`): NASA Planetary Fact Sheet, public domain.
- The repository contains **no** data from third-party websites. The public sites mentioned in
  the book are used only in the *Now try it on a real site* sections, on your own computer,
  under their own terms.

The book explains how to collect public data lawfully and politely. It is not legal advice.
