import requests

for code in [500, 200, 403]:
    r = requests.get(
        f"http://localhost:8000/trouble/status/{code}", timeout=10
    )
    try:
        r.raise_for_status()
        print(code, "ok")
    except requests.HTTPError as error:
        print(code, error)
