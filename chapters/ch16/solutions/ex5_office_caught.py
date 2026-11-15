from playwright.sync_api import sync_playwright

batches = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.on(
        "response",
        lambda r: (
            batches.append(r.json())
            if "category=Office" in r.url
            else None
        ),
    )
    page.goto("http://localhost:8000/shop/")
    page.wait_for_selector("div.product")
    page.select_option("#category", "Office")
    page.wait_for_function(
        "document.querySelector('#status').innerText.includes('of 30')"
    )
    for _ in range(20):
        if "Showing 30" in page.locator("#status").inner_text():
            break
        n = page.locator("div.product").count()
        page.mouse.wheel(0, 20000)
        page.wait_for_function(
            f"document.querySelectorAll('div.product').length > {n}",
            timeout=5000,
        )
    browser.close()
products = [p for b in batches for p in b["products"]]
prices = [p["price"] for p in products]
print(
    len(batches),
    "answers,",
    len(products),
    "products, average £" + f"{sum(prices) / len(prices):.2f}",
)
