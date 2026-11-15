r"""Exercise 15.3 (medium).

    Collect all 120 products with `per_page=50`, and print the number of requests, the number of products out of stock and the most reviewed product.

Expected output: chapters/ch15/expected/ex3_fewer_requests.txt
Solution: chapters/ch15/solutions/ex3_fewer_requests.py
"""
import time
import pandas as pd
import requests
url = "http://localhost:8000/shop/api/products"
products, page, pages, calls = [], 1, 1, 0

# Your code here
