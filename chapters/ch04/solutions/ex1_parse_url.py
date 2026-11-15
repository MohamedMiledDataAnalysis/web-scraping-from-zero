from urllib.parse import urlparse, parse_qs

parts = urlparse("http://localhost:8000/jobs/?q=python&city=London")
print(parts.hostname)
print(parts.path)
print(parse_qs(parts.query)["q"][0])
