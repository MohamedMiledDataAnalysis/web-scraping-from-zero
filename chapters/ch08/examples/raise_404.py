import requests

response = requests.get(
    "http://localhost:8000/library/page-51.html", timeout=10
)
response.raise_for_status()
print("This line is never reached")
