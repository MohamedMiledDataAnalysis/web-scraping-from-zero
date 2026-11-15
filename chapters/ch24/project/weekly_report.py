"""Weekly Excel report: open jobs, closed jobs, days online."""

import sqlite3

import pandas as pd

WEEK_END = "2027-03-07"
with sqlite3.connect("output/ch24/tracker.db") as db:
    jobs = pd.read_sql(
        "SELECT * FROM jobs",
        db,
        parse_dates=["first_seen", "last_seen"],
    )

jobs["posted"] = pd.to_datetime(jobs["posted"])
jobs["days_online"] = (jobs["last_seen"] - jobs["posted"]).dt.days + 1
jobs["status"] = (jobs["last_seen"] == WEEK_END).map(
    {True: "open", False: "closed"}
)
open_jobs = jobs[jobs["status"] == "open"].sort_values(
    ["salary_max", "title"], ascending=[False, True]
)
closed = jobs[jobs["status"] == "closed"]

skills = jobs["skills"].str.split(", ").explode().value_counts()
summary = pd.DataFrame(
    {
        "measure": [
            "jobs tracked",
            "still open",
            "closed this week",
            "average days online (closed jobs)",
            "most asked skill",
        ],
        "value": [
            len(jobs),
            len(open_jobs),
            len(closed),
            round(closed["days_online"].mean(), 1),
            skills.index[0],
        ],
    }
)
with pd.ExcelWriter("output/ch24/weekly_report.xlsx") as xl:
    summary.to_excel(xl, sheet_name="Summary", index=False)
    open_jobs.to_excel(xl, sheet_name="Open jobs", index=False)
    closed.to_excel(xl, sheet_name="Closed jobs", index=False)
    skills.rename("jobs").to_excel(xl, sheet_name="Skills")
print(summary.to_string(index=False))
print(
    open_jobs[["title", "city", "salary_max"]]
    .head(3)
    .to_string(index=False)
)
