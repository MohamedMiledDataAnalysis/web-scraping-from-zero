import datetime as dt
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, "chapters/ch25/project")
import logging  # noqa: E402

logging.getLogger("polite").setLevel(logging.WARNING)
from monitor import DB, run_day  # noqa: E402

Path(DB).unlink(missing_ok=True)
watch = pd.read_csv("output/ch25/watchlist.csv")
for n in range(14):
    day = (dt.date(2027, 3, 1) + dt.timedelta(days=n)).isoformat()
    for message in run_day(day, watch):
        print(day, message)
