r"""Exercise 12.1 (easy).

    Follow the *next* links of the quotes and print the number of pages and of quotes.

Expected output: chapters/ch12/expected/ex1_quotes_pages.txt
Solution: chapters/ch12/solutions/ex1_quotes_pages.py
"""
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
url, pages, quotes = "http://localhost:8000/quotes/", 0, 0

# Your code here
