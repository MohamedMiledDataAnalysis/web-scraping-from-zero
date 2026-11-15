from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8000/shop/")
    page.wait_for_selector("div.product")
    page.select_option("#category", "Garden")
    page.select_option("#sort", "price")
    page.wait_for_function(
        "document.querySelector('#status').innerText.includes('of 30')")
    names = page.locator("div.product h3.name").all_inner_texts()
    prices = page.locator("div.product p.price").all_inner_texts()
    for name, price in list(zip(names, prices))[:3]:
        print(price, name)
    print(page.locator("#status").inner_text())
    browser.close()
