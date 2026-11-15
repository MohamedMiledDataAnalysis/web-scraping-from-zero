import requests
from lxml import html as lh

tree = lh.fromstring(
    requests.get("http://localhost:8000/quotes/", timeout=10).content
)
authors = tree.xpath(
    '//div[@class="quote"][.//a[@class="tag" and text()="work"]]'
    '//small[@class="author"]/text()'
)
print(authors)
