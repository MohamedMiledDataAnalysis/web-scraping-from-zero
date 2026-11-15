"""Exercise 12.4 (harder).

    Visit the detail page of every book of the *Poetry* category and print the title of the book with the most pages, and the average rating of the category to two decimals. Reuse `book_parser.py`.

Expected output: chapters/ch12/expected/ex4_poetry.txt
Solution: chapters/ch12/solutions/ex4_poetry.py
"""
import sys
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
sys.path.insert(0, "chapters/ch12/examples")
from book_parser import parse_book_page  # noqa: E402

# Your code here
