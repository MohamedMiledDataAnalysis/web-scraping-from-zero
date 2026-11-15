import requests

print(requests.get("http://localhost:8000/robots.txt").text)
