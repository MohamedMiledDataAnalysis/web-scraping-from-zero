r"""Exercise 1.1 (easy).

    Copy `first_scraper.py` to `ex1_page2.py` and change it to print the books of page 2 of the library. The address of page 2 is `http://localhost:8000/library/page-2.html`. Expected first three lines:

Expected output: chapters/ch01/expected/ex1_page2.txt
Solution: chapters/ch01/solutions/ex1_page2.py
"""
import requests
from bs4 import BeautifulSoup
url = "http://localhost:8000/library/page-2.html"

# Your code here
