"""Check that the public websites used in the book still answer.

Run:  python check_real_sites.py

One request per address, one second apart, with a named User-Agent.
OK means the address answered with status 200. Anything else: see
reference/real_sites.md for an alternative.
"""
import time

import requests

HEADERS = {
    "User-Agent": "web-scraping-from-zero link check "
    "(+https://github.com/MohamedMiledDataAnalysis/web-scraping-from-zero)"
}

SITES = [
    ("Books to Scrape", "https://books.toscrape.com/"),
    ("Quotes to Scrape", "https://quotes.toscrape.com/"),
    ("Quotes, JavaScript version", "https://quotes.toscrape.com/js/"),
    ("Quotes, delayed JavaScript", "https://quotes.toscrape.com/js-delayed/"),
    ("Quotes, infinite scroll", "https://quotes.toscrape.com/scroll"),
    ("Quotes, login", "https://quotes.toscrape.com/login"),
    ("Scrape This Site, countries", "https://www.scrapethissite.com/pages/simple/"),
    ("Scrape This Site, hockey", "https://www.scrapethissite.com/pages/forms/"),
    ("Scrape This Site, AJAX",
     "https://www.scrapethissite.com/pages/ajax-javascript/"),
    ("Web Scraper test sites", "https://webscraper.io/test-sites"),
    ("The Internet", "https://the-internet.herokuapp.com/"),
    ("The Internet, dynamic loading",
     "https://the-internet.herokuapp.com/dynamic_loading/1"),
    ("Oxylabs Scraping Sandbox", "https://sandbox.oxylabs.io/products"),
    ("Real Python fake jobs", "https://realpython.github.io/fake-jobs/"),
    ("httpbin", "https://httpbin.org/get"),
    ("JSONPlaceholder", "https://jsonplaceholder.typicode.com/posts?userId=1"),
    ("Open-Meteo",
     "https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12"
     "&daily=temperature_2m_max"),
    ("data.gov.uk API", "https://data.gov.uk/api/action/package_search?q=fish"),
]

problems = 0
for name, url in SITES:
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        status = "OK" if r.status_code == 200 else f"status {r.status_code}"
    except requests.RequestException as e:
        status = type(e).__name__
    if status != "OK":
        problems += 1
    print(f"{status:<22} {name:<32} {url}")
    time.sleep(1)

print()
if problems:
    print(f"{problems} address(es) did not answer normally: "
          "see reference/real_sites.md for alternatives.")
else:
    print("Every address answered.")
