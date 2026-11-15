import requests

url = "http://localhost:8000/trouble/agent"
plain = requests.get(url, timeout=10)
print(plain.status_code, plain.request.headers["User-Agent"])

agent = "LearningScraper/1.0 (+mailto:reader@example.com)"
named = requests.get(url, headers={"User-Agent": agent}, timeout=10)
print(named.status_code, named.text)
