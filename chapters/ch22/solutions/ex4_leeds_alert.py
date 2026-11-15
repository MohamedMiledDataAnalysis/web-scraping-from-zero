import logging
import sys
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, "chapters/ch22/examples")
logging.getLogger("polite").setLevel(logging.WARNING)
from alert import send_alert  # noqa: E402
from daily_jobs import run  # noqa: E402
from toolkit.mailbox import start_test_mailbox  # noqa: E402

Path("output/ch22").mkdir(parents=True, exist_ok=True)
box = start_test_mailbox(quiet=True)
try:
    run("2027-03-05")
    new, _ = run("2027-03-06")
    hits = new[(new["city"] == "Leeds") & (new["salary_max"] >= 60000)]
    if len(hits):
        send_alert(
            f"Leeds: {len(hits)} well-paid new job(s)",
            "\n".join(
                f"{r.title} at {r.company}" for r in hits.itertuples()
            ),
        )
        text = sorted(Path("output/mailbox").glob("*.eml"))[
            -1
        ].read_text(encoding="utf-8")
        print(
            next(
                l for l in text.splitlines() if l.startswith("Subject:")
            )
        )
    else:
        print("No alert")
finally:
    box.stop()
