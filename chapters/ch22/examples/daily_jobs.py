"""Daily job board scraper: collect, check, store, compare."""

import logging
import sys
from urllib.parse import urljoin

from bs4 import BeautifulSoup

sys.path.insert(0, ".")
sys.path.insert(0, "chapters/ch22/examples")
from history import compare, save_day  # noqa: E402
from toolkit.polite import PoliteClient  # noqa: E402

log = logging.getLogger("daily")
DB = "output/ch22/jobs.db"
client = PoliteClient(
    "LearningScraper/1.0 (+mailto:reader@example.com)", delay=0.2
)


def collect(day):
    url, jobs = f"http://localhost:8000/jobs/?day={day}", []
    while url:
        soup = BeautifulSoup(client.get(url).text, "html.parser")
        for li in soup.select("li.job"):
            low, high = li.select_one("p.salary").text.split("–")
            jobs.append(
                {
                    "id": int(li["data-id"]),
                    "title": li.select_one("h2 a").text,
                    "company": li.select_one("p.company").text,
                    "city": li.select_one("p.location").text,
                    "salary_min": int(low.strip(" £").replace(",", "")),
                    "salary_max": int(
                        high.strip(" £").replace(",", "")
                    ),
                    "posted": li.select_one("time")["datetime"],
                }
            )
        nxt = soup.select_one("ul.pager li.next a")
        url = urljoin(url, nxt["href"]) + f"&day={day}" if nxt else None
    return jobs


def run(day):
    jobs = collect(day)
    announced = len(jobs)
    if announced == 0 or len({j["id"] for j in jobs}) != announced:
        raise RuntimeError(f"check failed on {day}: {announced} jobs")
    save_day(DB, day, jobs)
    new, removed = compare(DB, day)
    log.info(
        "%s: %d jobs, %d new, %d removed",
        day,
        announced,
        len(new),
        len(removed),
    )
    return new, removed
