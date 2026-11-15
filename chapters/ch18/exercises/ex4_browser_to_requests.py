"""Exercise 18.4 (harder).

    Log in with Playwright, copy the browser's cookies into a `requests.Session`, close the browser, and use the session to print the number of orders on `/account/`.

Expected output: chapters/ch18/expected/ex4_browser_to_requests.txt
Solution: chapters/ch18/solutions/ex4_browser_to_requests.py
"""
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# Your code here
