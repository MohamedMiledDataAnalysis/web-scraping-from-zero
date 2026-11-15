import requests

response = requests.get("http://localhost:8000/library/")
print(response.status_code, response.reason)
print(response.headers["Content-Type"])
print(len(response.text), "characters of HTML")
print(response.request.method, response.request.url)
print(response.request.headers["User-Agent"])
