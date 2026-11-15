from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(storage_state="output/ch18/state.json")
    page = context.new_page()
    page.goto("http://localhost:8000/account/")
    print(page.url)
    print(page.locator("#orders tbody tr").count(), "orders")
    browser.close()
