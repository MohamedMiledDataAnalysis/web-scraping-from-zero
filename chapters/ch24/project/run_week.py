import datetime as dt
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, "chapters/ch24/project")
from toolkit.mailbox import start_test_mailbox  # noqa: E402
from tracker import DB, run_day  # noqa: E402

logging.basicConfig(
    level=logging.INFO, format="%(message)s", stream=sys.stdout
)
logging.getLogger("polite").setLevel(logging.WARNING)
config = json.loads(Path("output/ch24/config.json").read_text())
Path(DB).unlink(missing_ok=True)
for old in Path("output/mailbox").glob(
    "*.eml"
):  # empty the test mailbox
    old.unlink()

box = start_test_mailbox(quiet=True)
try:
    for n in range(7):
        day = (dt.date(2027, 3, 1) + dt.timedelta(days=n)).isoformat()
        total, new_ids, subject = run_day(day, config)
        if subject:
            print("   email:", subject)
finally:
    box.stop()
print(
    len(list(Path("output/mailbox").glob("*.eml"))),
    "digest emails in the mailbox",
)
