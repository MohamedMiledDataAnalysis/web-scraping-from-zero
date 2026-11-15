r"""Exercise 1.4 (harder).

    Print only the books of page 1 that cost less than £15. The price text is `£26.93`: remove the `£` with `.replace("£", "")` and turn the rest into a number with `float()`.

Expected output: chapters/ch01/expected/ex4_cheap.txt
Solution: chapters/ch01/solutions/ex4_cheap.py
"""
import requests
from bs4 import BeautifulSoup

# Your code here
