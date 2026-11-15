r"""Exercise 15.4 (harder).

    Write a function `all_pages(url, params)` that collects every product for any category and sort, stops on the `pages` value, and never sends more than one request per 0.2 seconds. Use it to print, for each category, the cheapest product in stock.

Expected output: chapters/ch15/expected/ex4_cheapest.txt
Solution: chapters/ch15/solutions/ex4_cheapest.py
"""
import time
import pandas as pd
import requests
URL = "http://localhost:8000/shop/api/products"

# Your code here
