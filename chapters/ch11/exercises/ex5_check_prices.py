"""Exercise 11.5 (harder).

    Check that the visible price and the JSON-LD price of every book of page 1 are equal. Print the number of books checked and the number of differences.

Expected output: chapters/ch11/expected/ex5_check_prices.txt
Solution: chapters/ch11/solutions/ex5_check_prices.py
"""
import json
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
base = "http://localhost:8000/library/"

# Your code here
