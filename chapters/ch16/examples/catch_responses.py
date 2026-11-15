from playwright.sync_api import sync_playwright

caught = []


def on_response(response):
    if "/shop/api/products" in response.url and response.ok:
        caught.append(response.json())


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.on("response", on_response)
    page.goto("http://localhost:8000/shop/")
    with page.expect_response(lambda r: "category=Audio" in r.url):
        page.select_option("#category", "Audio")
    browser.close()

for data in caught:
    print(data["total"], "products, page", data["page"], "->",
          data["products"][0]["name"])
