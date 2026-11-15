import pandas as pd
import requests
from bs4 import BeautifulSoup

html = requests.get(
    "http://localhost:8000/trouble/messy-cards", timeout=10
).text
soup = BeautifulSoup(html, "html.parser")
records = []
for card in soup.select("div.card"):
    name = card.select_one("h3")
    price = card.select_one(".price")
    records.append(
        {
            "name": name.get_text(strip=True) if name else None,
            "price_text": price.get_text() if price else None,
        }
    )

df = pd.DataFrame(records)
print(df.to_string())
print(df.shape)
print(df.dtypes.to_string())
print(df.isna().sum().to_string())
