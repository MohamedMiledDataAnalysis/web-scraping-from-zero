# Cheat sheets

## requests

```python
import requests
session = requests.Session()
session.headers["User-Agent"] = "Name/1.0 (+mailto:you@example.com)"
r = session.get(url, params={"q": "x"}, timeout=15)
r.raise_for_status()                    # error on 4xx and 5xx
r.status_code, r.url, r.headers["Content-Type"], r.history
r.text          # str, with r.encoding     r.content   # bytes
r.json()        # dict or list
r = session.post(url, data={"field": "value"}, timeout=15)   # form
r = session.post(url, json={"key": "value"}, timeout=15)     # JSON body
with session.get(url, stream=True, timeout=60) as r:          # big file
    for chunk in r.iter_content(65536): f.write(chunk)
from urllib.parse import urljoin, urlparse, parse_qs
urljoin(page_url, href)
```

## BeautifulSoup

```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, "html.parser")          # or "lxml"
soup.find("div", class_="quote")                   # first or None
soup.find_all("a", href=True)                      # list
soup.find(id="x"); soup.find("div", attrs={"data-id": "3"})
soup.select("article.card p.price")                # list
soup.select_one("li.next a")                       # first or None
tag.get_text(" ", strip=True); tag["href"]; tag.get("href")
tag["class"]                                       # a list
tag.find_parent("article"); tag.find_next_sibling("td")
soup.find("th", string="Price")
soup.find("script", type="application/ld+json").string
```

## CSS selectors and XPath

| CSS | XPath | Means |
|---|---|---|
| `p` | `//p` | every `p` |
| `.price` | `//*[contains(@class, "price")]` | class |
| `#main` | `//*[@id="main"]` | id |
| `a[href]` | `//a[@href]` | has the attribute |
| `a[href^="/q/"]` | `//a[starts-with(@href, "/q/")]` | starts with |
| `a[href*="x"]` | `//a[contains(@href, "x")]` | contains |
| `div p` | `//div//p` | descendant |
| `ul > li` | `//ul/li` | child |
| `th + td` | `//th/following-sibling::td[1]` | next sibling |
| `li:nth-of-type(2)` | `//li[2]` | second |
| `div:has(.x)` | `//div[.//*[contains(@class,"x")]]` | contains an element |
| `:-soup-contains("Price")` | `//*[contains(text(), "Price")]` | text |
| (none) | `//p/..`, `//p/ancestor::div` | parent, ancestor |

Scrapy adds `::text` and `::attr(name)` to CSS: `response.css("a::attr(href)").getall()`.

## Playwright and Selenium

| Task | Playwright | Selenium |
|---|---|---|
| Start | `p.chromium.launch()` | `webdriver.Chrome(options=o)` |
| Open | `page.goto(url)` | `driver.get(url)` |
| Find | `page.locator(css)` | `driver.find_elements(By.CSS_SELECTOR, css)` |
| Text | `loc.inner_text()` | `el.text` |
| Click, type | `loc.click()`, `loc.fill(x)` | `el.click()`, `el.send_keys(x)` |
| Menu | `page.select_option(sel, v)` | `Select(el).select_by_value(v)` |
| Wait | automatic; `wait_for_selector` | `WebDriverWait(d, 10).until(EC...)` |
| Scroll | `page.mouse.wheel(0, 20000)` | `execute_script("window.scrollTo(...)")` |
| Catch JSON | `page.on("response", f)` | not built in |
| HTML | `page.content()` | `driver.page_source` |
| Close | `browser.close()` | `driver.quit()` |

## pandas for scraped data

```python
import pandas as pd
from io import StringIO
pd.read_html(StringIO(html), attrs={"id": "t"}, thousands=",", na_values=["n/a"])
df = pd.DataFrame(records); df.shape; df.dtypes; df.isna().sum()
df["price"] = df["price_text"].str.replace("£", "").str.replace(",", "").astype(float)
pd.read_csv(path, sep=";", decimal=",", thousands=".", encoding="utf-8")
pd.read_excel(path, sheet_name=None, header=None)      # look first
pd.json_normalize(api_records)
pd.to_datetime(s, format="%d/%m/%Y", errors="coerce")
df.drop_duplicates(subset="url"); df.dropna(subset=["title"])
df.groupby("category")["price"].agg(["count", "mean"])
df.to_csv(p, index=False); df.to_excel(p, index=False); df.to_sql("t", db)
```

## Regular expressions

| Pattern | Matches |
|---|---|
| `\d+` | a number |
| `[\d,]+(\.\d+)?` | a number with thousands commas and decimals |
| `\s+` | spaces, tabs, line breaks |
| `£\s*([\d,.]+)` | a pound amount, captured |
| `\((\d+) available\)` | the number in *(19 available)* |
| `\d{4}-\d{2}-\d{2}` | an ISO date |
| `var data = (\[.*?\]);` | a JSON array in a script (with `re.DOTALL`) |

`re.search(p, text).group(1)`, `re.findall(p, text)`, `re.sub(p, new, text)`; always `r"..."`.
