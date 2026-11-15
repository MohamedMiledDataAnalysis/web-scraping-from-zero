r"""Exercise 12.3 (medium).

    For each tag of the quotes (the tag box), visit its page and count its quotes. Remember that a tag page can have several pages. Print the five most used tags.

Expected output: chapters/ch12/expected/ex3_tag_counts.txt
Solution: chapters/ch12/solutions/ex3_tag_counts.py
"""
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
base = "http://localhost:8000/quotes/"
counts = {}

# Your code here
