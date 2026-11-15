import requests
from bs4 import BeautifulSoup

session = requests.Session()
library = BeautifulSoup(session.get("http://localhost:8000/library/",
                                    timeout=10).text, "html.parser")
print(len(library.select(".star-rating.Five")), "five-star books")
print(library.select_one('[data-id="7"] h3 a')["title"])
print(len(library.select("p.availability:not(.in-stock)")), "out of stock")
print(library.select_one("ul.pager > li.next > a")["href"])

quotes = BeautifulSoup(session.get("http://localhost:8000/quotes/",
                                   timeout=10).text, "html.parser")
tags = {a.text for a in quotes.select('.quote a[href^="/quotes/tag/"]')}
print(len(tags), "different tags on page 1")

book = BeautifulSoup(session.get(
    "http://localhost:8000/library/book/salt-kingdom-2.html",
    timeout=10).text, "html.parser")
print(book.select_one('th:-soup-contains("Price") + td').text)
print(book.select_one("ul.breadcrumb li:nth-of-type(3) a").text)
