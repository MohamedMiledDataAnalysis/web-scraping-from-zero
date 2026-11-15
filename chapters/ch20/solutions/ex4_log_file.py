import logging
import sys
from pathlib import Path

sys.path.insert(0, ".")
from toolkit.polite import PoliteClient  # noqa: E402

Path("output/ch20").mkdir(parents=True, exist_ok=True)
handler = logging.FileHandler("output/ch20/crawl.log", mode="w", encoding="utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
root = logging.getLogger()
root.setLevel(logging.INFO)
root.addHandler(handler)

client = PoliteClient("LearningScraper/1.0", delay=0.2, base_wait=0.3)
client.session.get("http://localhost:8000/trouble/flaky/reset", timeout=10)
for path in ["/library/", "/library/page-2.html", "/library/page-3.html", "/trouble/flaky"]:
    client.get("http://localhost:8000" + path)
    logging.info("done %s", path)
handler.close()

for line in open("output/ch20/crawl.log", encoding="utf-8"):
    time_stamp, level, message = line.rstrip("\n").split(" | ")
    if level == "WARNING":
        print(level, message)
