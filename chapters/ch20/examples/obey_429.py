import time

import requests

session = requests.Session()
delay = 0.0
for i in range(1, 9):
    r = session.get("http://localhost:8000/trouble/limited", timeout=10)
    if r.status_code == 429:
        wait = int(r.headers["Retry-After"])
        delay = max(delay * 2, 1.0)
        print(
            f"request {i}: 429, waiting {wait} s, "
            f"then {delay} s between requests"
        )
        time.sleep(wait)
        r = session.get(
            "http://localhost:8000/trouble/limited", timeout=10
        )
    print(f"request {i}: {r.status_code} {r.text}")
    time.sleep(delay)
