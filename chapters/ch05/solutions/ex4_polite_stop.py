import time
from urllib.robotparser import RobotFileParser

import requests

AGENT = "LearningScraper/1.0 (+mailto:reader@example.com)"
BASE = "http://localhost:8000"
robots = RobotFileParser(BASE + "/robots.txt")
robots.read()
delay = robots.crawl_delay(AGENT) or 1


def polite_get(url):
    if not robots.can_fetch(AGENT, url):
        print("Not allowed by robots.txt:", url)
        return None
    time.sleep(delay)
    response = requests.get(url, headers={"User-Agent": AGENT}, timeout=10)
    if response.status_code in (401, 403, 429):
        print("Stopping: status", response.status_code)
        return None
    return response


for path in ["/library/", "/trouble/status/403"]:
    r = polite_get(BASE + path)
    if r is not None:
        print(r.status_code, path)
