from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8000/quotes/js/")
    quotes = page.locator("div.quote span.text").all_inner_texts()
    print(len(quotes), "quotes")
    print(quotes[0])
    browser.close()
