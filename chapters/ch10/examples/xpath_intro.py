import requests
from lxml import html as lh

page = requests.get("http://localhost:8000/library/", timeout=10)
tree = lh.fromstring(page.content)

titles = tree.xpath('//article[contains(@class, "book-card")]/h3/a/@title')
print(len(titles), titles[:2])
prices = tree.xpath('//p[@class="price"]/text()')
print(prices[:3])
print(tree.xpath('string(//p[@class="result-count"])'))
