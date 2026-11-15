import requests

r = requests.get(
    "http://localhost:8000/files/eligible_assets.txt", timeout=10
)
print(repr(r.text[:30]))
print(repr(r.content.decode("utf-16").splitlines()[0]))
