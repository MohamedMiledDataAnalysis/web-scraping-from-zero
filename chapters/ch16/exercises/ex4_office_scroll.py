"""Exercise 16.4 (harder).

    Scroll the shop until all *Office* products are loaded (choose the category first), and print their number and their average price, read from the page.

Expected output: chapters/ch16/expected/ex4_office_scroll.txt
Solution: chapters/ch16/solutions/ex4_office_scroll.py
"""
from playwright.sync_api import sync_playwright
values = [float(t.replace("£", "")) for t in prices]

# Your code here
