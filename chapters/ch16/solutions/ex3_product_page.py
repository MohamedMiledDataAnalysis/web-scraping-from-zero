from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8000/shop/product/42")
    name = page.locator("h1.name").inner_text()
    price = page.locator("#product p.price").inner_text()
    stock = page.locator("#product p.stock").inner_text()
    print(name, price, stock)
    browser.close()
