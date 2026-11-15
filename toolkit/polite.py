"""PoliteClient: robots.txt, User-Agent, delay, timeout, retries, Retry-After, log."""
import logging
import time
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests

log = logging.getLogger("polite")
RETRY_STATUS = {429, 500, 502, 503, 504}


class NotAllowed(Exception):
    """robots.txt forbids this address, or the site refused us (401, 403)."""


class PoliteClient:
    def __init__(self, agent, delay=1.0, timeout=15, tries=4, base_wait=1.0):
        self.agent, self.delay, self.timeout = agent, delay, timeout
        self.tries, self.base_wait = tries, base_wait
        self.session = requests.Session()
        self.session.headers["User-Agent"] = agent
        self.robots = {}
        self.last_request = 0.0

    def allowed(self, url):
        root = "{0.scheme}://{0.netloc}".format(urlparse(url))
        if root not in self.robots:
            parser = RobotFileParser(root + "/robots.txt")
            parser.read()
            self.robots[root] = parser
            crawl_delay = parser.crawl_delay(self.agent)
            if crawl_delay and crawl_delay > self.delay:
                self.delay = float(crawl_delay)
        return self.robots[root].can_fetch(self.agent, url)

    def _wait_turn(self):
        pause = self.last_request + self.delay - time.monotonic()
        if pause > 0:
            time.sleep(pause)
        self.last_request = time.monotonic()

    def get(self, url, **kwargs):
        if not self.allowed(url):
            raise NotAllowed(f"robots.txt forbids {url}")
        for attempt in range(1, self.tries + 1):
            self._wait_turn()
            try:
                r = self.session.get(url, timeout=self.timeout, **kwargs)
            except (requests.Timeout, requests.ConnectionError) as error:
                reason, wait = type(error).__name__, None
            else:
                if r.status_code in (401, 403):
                    raise NotAllowed(f"status {r.status_code} for {url}")
                if r.status_code not in RETRY_STATUS:
                    return r
                reason = f"status {r.status_code}"
                wait = r.headers.get("Retry-After")
            if attempt == self.tries:
                log.error("Gave up on %s after %d tries (%s)", url, attempt, reason)
                raise RuntimeError(f"Gave up on {url} ({reason})")
            seconds = float(wait) if wait else self.base_wait * 2 ** (attempt - 1)
            log.warning("%s on %s, retry %d in %.1f s", reason, url, attempt, seconds)
            time.sleep(seconds)
