import requests

url = "http://localhost:8000/library/page-50.html"
response = requests.get(url, timeout=10)
response.raise_for_status()
print(response.status_code, len(response.text))
