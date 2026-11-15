from pathlib import Path

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

out = Path("output/ch16")
out.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8000/shop/")
    page.wait_for_selector("div.product")
    page.screenshot(path=out / "shop.png", full_page=True)
    html = page.content()
    browser.close()

soup = BeautifulSoup(html, "html.parser")
print(len(soup.select("div.product")), "products in the final HTML")
print(soup.select_one("div.product")["data-sku"])
print((out / "shop.png").exists())
