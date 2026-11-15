from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8000/shop/")
    page.wait_for_selector("div.product")
    with page.expect_response(lambda r: "sort=rating" in r.url and "Kitchen" in r.url):
        page.select_option("#category", "Kitchen")
        page.select_option("#sort", "rating")
    page.wait_for_function("document.querySelector('#status').innerText.includes('of 30')")
    cards = page.locator("div.product")
    for i in range(3):
        card = cards.nth(i)
        print(card.locator("p.rating").inner_text(), card.locator("h3").inner_text())
    browser.close()
