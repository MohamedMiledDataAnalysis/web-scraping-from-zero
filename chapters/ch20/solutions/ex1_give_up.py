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
        time.sleep(base_wait * 2 ** (attempt - 1))


try:
    get_with_retries("http://localhost:8000/trouble/status/500", tries=3, base_wait=0.2)
except RuntimeError as error:
    print(error)
