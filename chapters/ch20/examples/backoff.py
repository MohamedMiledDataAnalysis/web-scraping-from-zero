import time

import requests

RETRY_STATUS = {429, 500, 502, 503, 504}
session = requests.Session()


def get_with_retries(url, tries=4, base_wait=0.5):
    for attempt in range(1, tries + 1):
        try:
            r = session.get(url, timeout=10)
        except (requests.Timeout, requests.ConnectionError) as error:
            reason = type(error).__name__
        else:
            if r.status_code not in RETRY_STATUS:
                return r
            reason = f"status {r.status_code}"
        if attempt == tries:
            raise RuntimeError(f"Gave up after {tries} tries: {url} ({reason})")
        wait = base_wait * 2 ** (attempt - 1)
        print(f"  attempt {attempt}: {reason}, waiting {wait} s")
        time.sleep(wait)


session.get("http://localhost:8000/trouble/flaky/reset", timeout=10)
r = get_with_retries("http://localhost:8000/trouble/flaky")
print(r.status_code, r.text)
r = get_with_retries("http://localhost:8000/trouble/status/404")
print(r.status_code, "- not retried")
