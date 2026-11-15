import logging
import sys
from pathlib import Path

sys.path.insert(0, "chapters/ch22/examples")
Path("output/ch22").mkdir(parents=True, exist_ok=True)
Path("output/ch22/jobs.db").unlink(missing_ok=True)
logging.basicConfig(
    level=logging.INFO, format="%(message)s", stream=sys.stdout
)
logging.getLogger("polite").setLevel(logging.WARNING)

from daily_jobs import run  # noqa: E402

for day in [
    "2027-03-01",
    "2027-03-02",
    "2027-03-03",
    "2027-03-04",
    "2027-03-05",
]:
    new, removed = run(day)
    if len(new) and day != "2027-03-01":
        print(
            "   new:",
            ", ".join(new["title"].head(3)),
            "..." if len(new) > 3 else "",
        )
