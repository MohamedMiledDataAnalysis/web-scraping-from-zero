import time

import requests

session = requests.Session()
session.headers["X-API-Key"] = "pg-demo-2027"


def api_get(url, params=None, max_tries=5):
    """GET with a polite wait on 429, as the API asks in Retry-After."""
    for attempt in range(1, max_tries + 1):
        r = session.get(url, params=params, timeout=10)
        if r.status_code != 429:
            r.raise_for_status()
            return r.json()
        wait = int(r.headers.get("Retry-After", 5))
        print(f"429 on attempt {attempt}: waiting {wait} s as asked")
        time.sleep(wait)
    raise RuntimeError(f"Still limited after {max_tries} tries: {url}")


url = "http://localhost:8000/api/v1/stations"
for i in range(1, 13):
    data = api_get(url)
print("12 calls done,", data["count"], "stations each time")
