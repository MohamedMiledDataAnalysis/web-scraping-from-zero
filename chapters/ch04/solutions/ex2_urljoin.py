from urllib.parse import urljoin

base = "http://localhost:8000/library/category/history/page-3.html"
for link in [
    "page-2.html",
    "../fiction/",
    "/library/book/salt-kingdom-2.html",
]:
    print(urljoin(base, link))
