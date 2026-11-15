import logging
import sys
from pathlib import Path

sys.path.insert(0, "chapters/ch22/examples")
logging.getLogger("polite").setLevel(logging.WARNING)
import daily_jobs  # noqa: E402
from history import compare, save_day  # noqa: E402

db = "output/ch22/ex1.db"
Path(db).parent.mkdir(parents=True, exist_ok=True)
Path(db).unlink(missing_ok=True)
for day in ["2027-03-01", "2027-03-10"]:
    save_day(db, day, daily_jobs.collect(day))
new, removed = compare(db, "2027-03-10")
print(len(new), "new,", len(removed), "removed")
