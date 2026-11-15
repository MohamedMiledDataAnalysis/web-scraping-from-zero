import requests

session = requests.Session()
session.headers.update(
    {"User-Agent": "LearningScraper/1.0 (+mailto:reader@example.com)"}
)

for page in range(1, 11):
    r = session.get(
        f"http://localhost:8000/library/page-{page}.html", timeout=10
    )
    r.raise_for_status()
print("10 pages with a session:", r.status_code)
print("User-Agent sent:", r.request.headers["User-Agent"])
