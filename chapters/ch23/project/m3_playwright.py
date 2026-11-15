"""Method 3: Playwright on the 50 list pages (for comparison only)."""
import json
import time
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

OUT = Path("output/ch23")
rows, loads = [], 0
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(user_agent="LearningScraper/1.0 (+mailto:reader@example.com)")
    counter = {"n": 0}
    page.on("request", lambda r: counter.__setitem__("n", counter["n"] + 1))
    page.goto("http://localhost:8000/library/")
    while True:
        loads += 1
        soup = BeautifulSoup(page.content(), "html.parser")
        for card in soup.select("article.book-card"):
            rows.append({"title": card.select_one("h3 a")["title"],
                         "price": float(card.select_one("p.price").text[1:])})
        nxt = page.locator("ul.pager li.next a")
        if nxt.count() == 0:
            break
        time.sleep(0.2)
        nxt.click()
        page.wait_for_load_state()
    browser.close()

pd.DataFrame(rows).to_csv(OUT / "m3_playwright.csv", index=False)
(OUT / "m3_meta.json").write_text(json.dumps({"requests": counter["n"]}))
print(len(rows), "books,", loads, "pages loaded,", counter["n"], "requests by the browser")
