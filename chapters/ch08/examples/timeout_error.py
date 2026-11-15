import requests

requests.get("http://localhost:8000/trouble/slow?seconds=3", timeout=1)
