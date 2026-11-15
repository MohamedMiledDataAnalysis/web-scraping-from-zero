import logging
import sys

sys.path.insert(0, ".")
from toolkit.polite import PoliteClient  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-7s %(message)s",
    stream=sys.stdout,
)
client = PoliteClient(
    "LearningScraper/1.0", delay=0.2, timeout=1, tries=2, base_wait=0.2
)
try:
    client.get("http://localhost:8000/trouble/slow?seconds=2")
except RuntimeError as error:
    print(error)
