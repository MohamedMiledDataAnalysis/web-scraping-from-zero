import logging
import sys
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, "chapters/ch22/examples")
from alert import send_alert  # noqa: E402
from daily_jobs import run  # noqa: E402
from toolkit.mailbox import start_test_mailbox  # noqa: E402

logging.basicConfig(level=logging.WARNING, stream=sys.stdout)
Path("output/ch22").mkdir(parents=True, exist_ok=True)
box = start_test_mailbox()
try:
    run("2027-03-05")
    new, removed = run("2027-03-06")
    wanted = new[new["title"].str.contains("Analyst|Developer")]
    if len(wanted):
        lines = [f"- {r.title}, {r.company}, {r.city}, up to £{r.salary_max:,}"
                 for r in wanted.itertuples()]
        send_alert(f"{len(wanted)} new analyst or developer jobs on 2027-03-06",
                   "\n".join(lines))
finally:
    box.stop()
message = sorted(Path("output/mailbox").glob("*.eml"))[-1].read_text(encoding="utf-8")
print(message.split("\n\n", 1)[1].strip())
