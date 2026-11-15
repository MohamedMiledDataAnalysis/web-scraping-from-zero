"""Exercise 11.3 (medium).

    Print, from its JSON-LD, the name, price and availability (*InStock* or *OutOfStock*) of the books with ids 1 to 5. Their addresses are in the cards of page 1.

Expected output: chapters/ch11/expected/ex3_ld_five.txt
Solution: chapters/ch11/solutions/ex3_ld_five.py
"""
import json
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
base = "http://localhost:8000/library/"

# Your code here
