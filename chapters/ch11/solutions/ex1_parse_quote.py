import requests
from bs4 import BeautifulSoup


def parse_quote(div):
    text = div.select_one("span.text")
    author = div.select_one("small.author")
    return {
        "text": text.text.strip("“”") if text else None,
        "author": author.text if author else None,
        "tags": [a.text for a in div.select("a.tag")],
    }


html = requests.get("http://localhost:8000/quotes/page/2/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")
for div in soup.select("div.quote")[:2]:
    print(parse_quote(div))
