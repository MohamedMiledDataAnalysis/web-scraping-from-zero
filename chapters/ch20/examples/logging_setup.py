import logging
import sys
from pathlib import Path

Path("output/ch20").mkdir(parents=True, exist_ok=True)
log = logging.getLogger("scraper")
log.setLevel(logging.INFO)
screen = logging.StreamHandler(sys.stdout)
screen.setFormatter(logging.Formatter("%(levelname)-7s %(message)s"))
file = logging.FileHandler(
    "output/ch20/scraper.log", mode="w", encoding="utf-8"
)
file.setFormatter(
    logging.Formatter("%(asctime)s %(levelname)-7s %(message)s")
)
log.addHandler(screen)
log.addHandler(file)

log.info("Starting: %d pages to visit", 50)
log.warning("Retrying %s after status %d", "/trouble/flaky", 503)
log.error("Gave up on %s", "/trouble/slow?seconds=30")
log.debug("Not shown: below the INFO level")
print(
    open("output/ch20/scraper.log", encoding="utf-8")
    .read()
    .count("\n"),
    "lines in the file",
)
