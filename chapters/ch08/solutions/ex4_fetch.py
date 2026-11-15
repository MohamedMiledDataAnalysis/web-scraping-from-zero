import requests


def fetch(session, url, timeout=2):
    try:
        r = session.get(url, timeout=timeout)
        r.raise_for_status()
    except requests.Timeout:
        print("Timeout:", url)
        return None
    except requests.HTTPError as error:
        print("Error:", error)
        return None
    return r.text


session = requests.Session()
for path in ["/library/", "/trouble/slow?seconds=5", "/trouble/status/404"]:
    html = fetch(session, "http://localhost:8000" + path)
    if html is not None:
        print("Got", len(html), "characters from", path)
