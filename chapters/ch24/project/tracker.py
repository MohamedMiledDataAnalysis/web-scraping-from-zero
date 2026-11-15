"""Daily job tracker: collect, details for new jobs, update, digest."""
import json
import logging
import sqlite3
import sys
from urllib.parse import urljoin

from bs4 import BeautifulSoup

sys.path.insert(0, ".")
sys.path.insert(0, "chapters/ch22/examples")
from alert import send_alert  # noqa: E402
from toolkit.polite import PoliteClient  # noqa: E402

log = logging.getLogger("tracker")
BASE = "http://localhost:8000/jobs/"
DB = "output/ch24/tracker.db"
client = PoliteClient("JobTracker/1.0 (+mailto:reader@example.com)", delay=0.2)

SCHEMA = """CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY, title TEXT, company TEXT, city TEXT,
    salary_min INTEGER, salary_max INTEGER, skills TEXT, posted TEXT,
    first_seen TEXT, last_seen TEXT)"""


def money(text):
    return int(text.strip(" £").replace(",", ""))


def collect_list(day, query):
    """Every job of the board for one search word on one day: {id: summary}."""
    found, page = {}, 1
    while True:
        url = f"{BASE}?q={query}&day={day}&page={page}"
        soup = BeautifulSoup(client.get(url).text, "html.parser")
        for li in soup.select("li.job"):
            low, high = li.select_one("p.salary").text.split("–")
            found[int(li["data-id"])] = {
                "title": li.select_one("h2 a").text, "city": li.select_one("p.location").text,
                "company": li.select_one("p.company").text,
                "salary_min": money(low), "salary_max": money(high),
                "posted": li.select_one("time")["datetime"]}
        if not soup.select_one("ul.pager li.next a"):
            return found
        page += 1


def fetch_details(day, job_id):
    soup = BeautifulSoup(client.get(f"{BASE}{job_id}/?day={day}").text, "html.parser")
    return soup.select_one("dd.skills").text


def matches(job, config):
    return job["city"] in config["cities"] and job["salary_max"] >= config["min_salary"]


def update_db(day, jobs):
    """Insert new jobs, refresh last_seen of known ones; return the new ids."""
    with sqlite3.connect(DB) as db:
        db.execute(SCHEMA)
        known = {r[0] for r in db.execute("SELECT id FROM jobs")}
        new_ids = [i for i in jobs if i not in known]
        for job_id in new_ids:
            j = jobs[job_id]
            db.execute("INSERT INTO jobs VALUES (?,?,?,?,?,?,?,?,?,?)",
                       (job_id, j["title"], j["company"], j["city"], j["salary_min"],
                        j["salary_max"], j["skills"], j["posted"], day, day))
        db.executemany("UPDATE jobs SET last_seen = ? WHERE id = ?",
                       [(day, i) for i in jobs if i in known])
    return new_ids


def digest(day, jobs, new_ids, config):
    if not new_ids:
        return None
    lines = [f"- {jobs[i]['title']} | {jobs[i]['company']} | {jobs[i]['city']} | "
             f"£{jobs[i]['salary_min']:,}–£{jobs[i]['salary_max']:,} | {jobs[i]['skills']}"
             for i in sorted(new_ids)]
    subject = f"{len(new_ids)} new job(s) for you on {day}"
    send_alert(subject, "\n".join(lines))
    return subject


def run_day(day, config, with_email=True):
    jobs = {}
    for query in config["searches"]:
        jobs.update(collect_list(day, query))
    jobs = {i: j for i, j in jobs.items() if matches(j, config)}
    with sqlite3.connect(DB) as db:
        db.execute(SCHEMA)
        known = {r[0] for r in db.execute("SELECT id FROM jobs")}
    for job_id in jobs:
        if job_id not in known:
            jobs[job_id]["skills"] = fetch_details(day, job_id)
    new_ids = update_db(day, jobs)
    log.info("%s: %d matching jobs, %d new", day, len(jobs), len(new_ids))
    subject = digest(day, jobs, new_ids, config) if with_email else None
    return len(jobs), new_ids, subject
