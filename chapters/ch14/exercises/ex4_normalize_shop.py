"""Exercise 14.4 (medium).

    The hidden shop API of Chapter 15 also answers without a key: `http://localhost:8000/shop/api/products?per_page=5`. Flatten its answer with `json_normalize` and print the columns, then the names of the products in stock.

Expected output: chapters/ch14/expected/ex4_normalize_shop.txt
Solution: chapters/ch14/solutions/ex4_normalize_shop.py
"""
import pandas as pd
import requests

# Your code here
