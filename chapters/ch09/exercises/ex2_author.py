"""Exercise 9.2 (easy).

    On the author page `http://localhost:8000/quotes/author/tomas-reyna/`, print the author's name, birth year and birthplace.

Expected output: chapters/ch09/expected/ex2_author.txt
Solution: chapters/ch09/solutions/ex2_author.py
"""
import requests
from bs4 import BeautifulSoup
url = "http://localhost:8000/quotes/author/tomas-reyna/"

# Your code here
