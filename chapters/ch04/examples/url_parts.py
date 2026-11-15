from urllib.parse import urlparse, parse_qs

url = "http://localhost:8000/jobs/?city=Leeds&page=2#results"
parts = urlparse(url)
print(parts.scheme, parts.hostname, parts.port)
print(parts.path)
print(parts.query)
print(parse_qs(parts.query))
print(parts.fragment)
