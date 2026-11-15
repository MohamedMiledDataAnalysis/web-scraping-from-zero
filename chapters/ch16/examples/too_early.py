from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8000/shop/")
    print("Right after goto:", page.locator("div.product").count())
    page.wait_for_selector("div.product")
    print("After waiting:", page.locator("div.product").count())
    print(page.locator("#status").inner_text())
    browser.close()
