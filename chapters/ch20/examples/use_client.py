import logging
import sys

sys.path.insert(0, ".")
from toolkit.polite import NotAllowed, PoliteClient  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(levelname)-7s %(message)s",
                    stream=sys.stdout)
client = PoliteClient("LearningScraper/1.0 (+mailto:reader@example.com)",
                      delay=0.2, base_wait=0.5)
client.session.get("http://localhost:8000/trouble/flaky/reset", timeout=10)

for path in ["/library/", "/trouble/flaky", "/private/", "/trouble/status/403",
             "/trouble/status/404"]:
    try:
        r = client.get("http://localhost:8000" + path)
        print(r.status_code, path)
    except NotAllowed as error:
        print("Not allowed:", error)
