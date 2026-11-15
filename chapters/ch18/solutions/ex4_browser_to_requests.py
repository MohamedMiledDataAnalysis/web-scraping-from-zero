import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8000/account/login")
    page.get_by_label("Username").fill("reader")
    page.get_by_label("Password").fill("practice")
    page.get_by_role("button", name="Log in").click()
    page.wait_for_url("**/account/")
    cookies = context.cookies()
    browser.close()

session = requests.Session()
for c in cookies:
    session.cookies.set(c["name"], c["value"])
soup = BeautifulSoup(session.get("http://localhost:8000/account/", timeout=10).text,
                     "html.parser")
print(len(soup.select("#orders tbody tr")), "orders, read without a browser")
