"""Exercise 18.2 (medium).

    Write a function `login(session, username, password)` that returns `True` when the login worked (the page shows the user's name in `#user-name`) and `False` otherwise. Test it with the right and the wrong password, each in a new session.

Expected output: chapters/ch18/expected/ex2_login_function.txt
Solution: chapters/ch18/solutions/ex2_login_function.py
"""
import requests
from bs4 import BeautifulSoup
BASE = "http://localhost:8000"

# Your code here
