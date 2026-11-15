"""Job board history in SQLite: one row per job per day."""

import sqlite3

import pandas as pd

SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    day TEXT NOT NULL, id INTEGER NOT NULL,
    title TEXT, company TEXT, city TEXT,
    salary_min INTEGER, salary_max INTEGER, posted TEXT,
    PRIMARY KEY (day, id)
)"""


def save_day(db_path, day, jobs):
    """Store the jobs seen on `day`; a second run replaces that day."""
    with sqlite3.connect(db_path) as db:
        db.execute(SCHEMA)
        db.execute("DELETE FROM jobs WHERE day = ?", (day,))
        frame = pd.DataFrame(jobs).assign(day=day)
        frame.to_sql("jobs", db, if_exists="append", index=False)


def compare(db_path, day):
    """New and removed jobs between `day` and the previous stored day."""
    with sqlite3.connect(db_path) as db:
        days = [
            r[0]
            for r in db.execute(
                "SELECT DISTINCT day FROM jobs WHERE day < ? "
                "ORDER BY day DESC LIMIT 1",
                (day,),
            )
        ]
        today = pd.read_sql(
            "SELECT * FROM jobs WHERE day = ? ORDER BY id",
            db,
            params=(day,),
        )
        if not days:
            return today, today.iloc[0:0]
        before = pd.read_sql(
            "SELECT * FROM jobs WHERE day = ? ORDER BY id",
            db,
            params=(days[0],),
        )
    new = today[~today["id"].isin(before["id"])]
    removed = before[~before["id"].isin(today["id"])]
    return new, removed
