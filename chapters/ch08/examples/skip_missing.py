import requests

for page in [49, 50, 51]:
    url = f"http://localhost:8000/library/page-{page}.html"
    response = requests.get(url, timeout=10)
    try:
        response.raise_for_status()
    except requests.HTTPError as error:
        print("Skipped:", error)
        continue
    print("Page", page, "ok")
