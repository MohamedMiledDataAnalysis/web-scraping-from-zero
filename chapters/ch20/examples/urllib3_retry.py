import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

retry = Retry(total=4, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504],
              allowed_methods=["GET"], respect_retry_after_header=True)
session = requests.Session()
session.mount("http://", HTTPAdapter(max_retries=retry))
session.mount("https://", HTTPAdapter(max_retries=retry))

session.get("http://localhost:8000/trouble/flaky/reset", timeout=10)
r = session.get("http://localhost:8000/trouble/flaky", timeout=10)
print(r.status_code, r.text)
