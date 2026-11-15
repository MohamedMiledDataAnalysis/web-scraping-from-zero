import sys

import pandas as pd

sys.path.insert(0, "chapters/ch25/project")
from monitor import alerts_for  # noqa: E402

watch = pd.read_csv("output/ch25/watchlist.csv")
watch["target"] = (watch["target"] * 1.05).round(2)
for message in alerts_for("2027-03-10", watch) or ["No alert"]:
    print(message)
