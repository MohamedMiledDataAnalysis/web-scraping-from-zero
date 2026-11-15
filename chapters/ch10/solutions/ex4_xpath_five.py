import requests
from lxml import html as lh

page = requests.get("http://localhost:8000/library/", timeout=10)
tree = lh.fromstring(page.content)
for title in tree.xpath(
    '//article[.//p[contains(@class, "Five")]]//h3/a/@title'
):
    print(title)
