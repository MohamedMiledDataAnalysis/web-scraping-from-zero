import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, "chapters/ch24/project")
logging.getLogger("polite").setLevel(logging.WARNING)
from tracker import collect_list, matches  # noqa: E402

config = json.loads(Path("output/ch24/config.json").read_text())
for searches in [config["searches"], config["searches"] + ["sql"]]:
    jobs = {}
    for q in searches:
        jobs.update(collect_list("2027-03-07", q))
    print(
        searches,
        "->",
        sum(matches(j, config) for j in jobs.values()),
        "matching jobs",
    )
