import csv
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

OUT = Path("output/ch12/pages_progress.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)
FIELDS = ["page", "books", "first_title"]

done = set()
if OUT.exists():
    with open(OUT, encoding="utf-8") as f:
        done = {int(row["page"]) for row in csv.DictReader(f)}
print("Already done:", len(done), "pages")

session = requests.Session()
new_file = not OUT.exists()
with open(OUT, "a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS)
    if new_file:
        writer.writeheader()
    for page in range(1, 11):
        if page in done:
            continue
        url = f"http://localhost:8000/library/page-{page}.html"
        soup = BeautifulSoup(
            session.get(url, timeout=10).text, "html.parser"
        )
        cards = soup.select("article.book-card h3 a")
        writer.writerow(
            {
                "page": page,
                "books": len(cards),
                "first_title": cards[0]["title"],
            }
        )
        f.flush()
        time.sleep(0.2)
        if page == 6:
            print("Simulated crash after page 6")
            break
