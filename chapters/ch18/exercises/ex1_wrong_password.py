r"""Exercise 18.1 (easy).

    Try to log in with the right token but the password `wrong`. Print the status code and the error message.

Expected output: chapters/ch18/expected/ex1_wrong_password.txt
Solution: chapters/ch18/solutions/ex1_wrong_password.py
"""
import requests
from bs4 import BeautifulSoup
BASE = "http://localhost:8000"

# Your code here
