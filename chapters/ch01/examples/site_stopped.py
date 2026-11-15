import requests

# The same request, sent to a port where no site is running.
page = requests.get("http://localhost:8999/library/")
