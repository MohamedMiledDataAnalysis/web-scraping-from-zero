"""Exercise 9.5 (harder).

    Build a dictionary of the information table of the book `the-broken-forest-1`, then print the stock as a number (from `In stock (19 available)`) and the number of pages as a number.

Expected output: chapters/ch09/expected/ex5_book_info.txt
Solution: chapters/ch09/solutions/ex5_book_info.py
"""
import requests
from bs4 import BeautifulSoup
url = "http://localhost:8000/library/book/the-broken-forest-1.html"
info = {row.th.text: row.td.text
        for row in soup.find("table", class_="info").find_all("tr")}

# Your code here
