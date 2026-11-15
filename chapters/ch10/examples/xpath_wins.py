import requests
from lxml import html as lh

url = "http://localhost:8000/library/book/salt-kingdom-2.html"
tree = lh.fromstring(requests.get(url, timeout=10).content)
print(tree.xpath('//th[text()="Pages"]/following-sibling::td[1]/text()'))

library = lh.fromstring(requests.get("http://localhost:8000/library/",
                                     timeout=10).content)
cards = library.xpath('//p[contains(@class, "Five")]/ancestor::article')
print([c.get("data-id") for c in cards])
out = library.xpath('//p[contains(text(), "Out of stock")]'
                    '/ancestor::article//h3/a/@title')
print(out)
