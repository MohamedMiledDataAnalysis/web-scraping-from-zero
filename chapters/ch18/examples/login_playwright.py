from pathlib import Path

from playwright.sync_api import sync_playwright

state_file = Path("output/ch18/state.json")
state_file.parent.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8000/account/login")
    page.get_by_label("Username").fill("reader")
    page.get_by_label("Password").fill("practice")
    page.get_by_role("button", name="Log in").click()
    page.wait_for_url("**/account/")
    print(page.locator("h1").inner_text())
    context.storage_state(path=state_file)
    browser.close()
print("Saved login:", state_file.exists())
