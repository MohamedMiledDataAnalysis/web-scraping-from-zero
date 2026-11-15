import time
from urllib.robotparser import RobotFileParser

import requests

AGENT = "LearningScraper/1.0 (+mailto:reader@example.com)"
BASE = "http://localhost:8000"

robots = RobotFileParser(BASE + "/robots.txt")
robots.read()
delay = robots.crawl_delay(AGENT) or 0.2   # 0.2 s: the site's terms


def polite_get(url):
    """Fetch url if robots.txt allows it, after waiting the crawl delay."""
    if not robots.can_fetch(AGENT, url):
        print("Not allowed by robots.txt:", url)
        return None
    time.sleep(delay)
    return requests.get(url, headers={"User-Agent": AGENT}, timeout=10)


for path in ["/library/", "/private/", "/library/page-2.html"]:
    response = polite_get(BASE + path)
    if response is not None:
        print(response.status_code, path)
