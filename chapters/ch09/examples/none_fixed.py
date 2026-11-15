import requests
from bs4 import BeautifulSoup


def text_or_none(parent, *args, **kwargs):
    """Text of the first match inside parent, or None if there is none."""
    found = parent.find(*args, **kwargs)
    return found.get_text(" ", strip=True) if found else None


html = requests.get(
    "http://localhost:8000/trouble/messy-cards", timeout=10
).text
soup = BeautifulSoup(html, "html.parser")
for card in soup.find_all("div", class_="card"):
    name = text_or_none(card, "h3", class_="name")
    price = text_or_none(card, "span", class_="price")
    print(f"{str(name):<12} {price!r}")
