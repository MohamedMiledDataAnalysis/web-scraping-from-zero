"""Entry point for the scheduler (Chapter 22)."""

import datetime as dt
import logging
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
os.chdir(ROOT)  # the scheduler starts elsewhere
sys.path.insert(0, str(ROOT / "chapters/ch22/examples"))
Path("output/ch22").mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename="output/ch22/daily.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

from daily_jobs import run  # noqa: E402

try:
    run(dt.date.today().isoformat())
except Exception:
    logging.exception("Daily job failed")
    sys.exit(1)
