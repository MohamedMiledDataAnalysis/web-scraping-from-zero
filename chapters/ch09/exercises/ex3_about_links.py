"""Exercise 9.3 (medium).

    For each quote of page 1 of the quotes, print the author and the address of the author's *about* page, made complete with `urljoin`. Expected first three lines:

Expected output: chapters/ch09/expected/ex3_about_links.txt
Solution: chapters/ch09/solutions/ex3_about_links.py
"""
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
url = "http://localhost:8000/quotes/"

# Your code here
