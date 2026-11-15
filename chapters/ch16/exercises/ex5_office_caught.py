"""Exercise 16.5 (harder).

    Do exercise 16.4 again by catching the API answers instead of reading the page. Count the API answers you caught.

Expected output: chapters/ch16/expected/ex5_office_caught.txt
Solution: chapters/ch16/solutions/ex5_office_caught.py
"""
from playwright.sync_api import sync_playwright
batches = []
products = [p for b in batches for p in b["products"]]
prices = [p["price"] for p in products]

# Your code here
