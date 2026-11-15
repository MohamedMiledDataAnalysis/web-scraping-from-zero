"""Exercise 4.3 (medium).

    Request `http://localhost:8000/library/page-51.html` (the library has only 50 pages) and print the status code, whether the response is `ok`, and the text of its `h1`.

Expected output: chapters/ch04/expected/ex3_404.txt
Solution: chapters/ch04/solutions/ex3_404.py
"""
import requests
from bs4 import BeautifulSoup

# Your code here
