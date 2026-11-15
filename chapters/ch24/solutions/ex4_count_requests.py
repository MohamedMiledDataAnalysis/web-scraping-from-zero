import datetime as dt
import json
import logging
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, "chapters/ch24/project")
logging.getLogger("polite").setLevel(logging.WARNING)
import tracker  # noqa: E402

counts = Counter()
original_get = tracker.client.get


def counting_get(url, **kwargs):
    counts["detail pages" if "/?day=" in url else "list pages"] += 1
    return original_get(url, **kwargs)


tracker.client.get = counting_get
tracker.DB = "output/ch24/count.db"
Path(tracker.DB).unlink(missing_ok=True)
config = json.loads(Path("output/ch24/config.json").read_text())
for n in range(7):
    tracker.run_day((dt.date(2027, 3, 1) + dt.timedelta(n)).isoformat(), config,
                    with_email=False)
print(dict(counts), "| total:", sum(counts.values()))
