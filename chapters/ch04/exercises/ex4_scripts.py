r"""Exercise 4.4 (medium).

    Use the Elements panel on a book page of the library (click any title). Find the tag and the attributes of the script that contains `"@type": "Book"`. Then confirm it in Python: print the `type` attribute of every `script` tag of `http://localhost:8000/library/book/salt-kingdom-2.html`.

Expected output: chapters/ch04/expected/ex4_scripts.txt
Solution: chapters/ch04/solutions/ex4_scripts.py
"""
import requests
from bs4 import BeautifulSoup
url = "http://localhost:8000/library/book/salt-kingdom-2.html"

# Your code here
