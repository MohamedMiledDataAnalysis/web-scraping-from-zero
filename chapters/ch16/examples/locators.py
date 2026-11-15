from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8000/quotes/js/")
    cards = page.locator("div.quote")
    print(cards.count(), "cards")
    first = cards.first
    print(first.locator("small.author").inner_text())
    print(first.locator("a.tag").all_inner_texts())
    page.get_by_role("link", name="next").click()
    print(page.url)
    print(page.locator("div.quote small.author").first.inner_text())
    browser.close()
