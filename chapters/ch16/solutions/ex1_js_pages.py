from playwright.sync_api import sync_playwright

texts, authors = [], []
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8000/quotes/js/")
    while True:
        page.wait_for_selector("div.quote")
        texts += page.locator("div.quote span.text").all_inner_texts()
        authors += page.locator("div.quote small.author").all_inner_texts()
        next_link = page.locator("li.next a")
        if next_link.count() == 0:
            break
        next_link.click()
        page.wait_for_load_state()
    browser.close()
print(len(texts), "quotes; last author:", authors[-1])
