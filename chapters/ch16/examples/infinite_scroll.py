from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 800})
    page.goto("http://localhost:8000/shop/")
    page.wait_for_selector("div.product")
    previous = 0
    while True:
        count = page.locator("div.product").count()
        if count == previous:
            break
        previous = count
        page.mouse.wheel(0, 20000)                 # scroll down a lot
        try:
            page.wait_for_function(
                f"document.querySelectorAll('div.product').length > {count}",
                timeout=3000)
        except Exception:
            pass                                   # nothing more came
    print(page.locator("div.product").count(), "products after scrolling")
    print(page.locator("#status").inner_text())
    browser.close()
