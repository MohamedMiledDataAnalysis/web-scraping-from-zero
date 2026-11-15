import requests

r = requests.get("http://localhost:8000/trouble/wrong-charset", timeout=10)
print(r.headers["Content-Type"])
print(r.encoding, "->", r.text)
print(r.apparent_encoding)
r.encoding = "utf-8"
print(r.encoding, "->", r.text)
