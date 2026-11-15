import requests

for seconds in [0.5, 3]:
    url = f"http://localhost:8000/trouble/slow?seconds={seconds}"
    try:
        r = requests.get(url, timeout=2)
        print(seconds, "->", r.status_code)
    except requests.Timeout:
        print(seconds, "-> gave up after 2 seconds")
