import requests

for code in [200, 404, 429, 503]:
    r = requests.get(f"http://localhost:8000/trouble/status/{code}")
    print(code, "->", r.status_code, r.reason, "| ok:", r.ok)

r = requests.get("http://localhost:8000/trouble/old-page")
print(r.status_code, r.url)
print([h.status_code for h in r.history])
