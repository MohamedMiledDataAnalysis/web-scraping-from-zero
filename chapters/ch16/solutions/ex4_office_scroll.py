from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8000/shop/")
    page.wait_for_selector("div.product")
    page.select_option("#category", "Office")
    page.wait_for_function("document.querySelector('#status').innerText.includes('of 30')")
    while "Showing 30" not in page.locator("#status").inner_text():
        page.mouse.wheel(0, 20000)
        page.wait_for_timeout(300)
    prices = page.locator("div.product p.price").all_inner_texts()
    browser.close()
values = [float(t.replace("£", "")) for t in prices]
print(len(values), "products, average £" + f"{sum(values) / len(values):.2f}")
