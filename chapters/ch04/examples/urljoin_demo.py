from urllib.parse import urljoin

page = "http://localhost:8000/library/page-7.html"
print(urljoin(page, "page-8.html"))
print(urljoin(page, "book/salt-kingdom-2.html"))
print(urljoin(page, "/quotes/"))
print(urljoin(page, "../tables/"))
print(urljoin(page, "https://books.toscrape.com/"))
