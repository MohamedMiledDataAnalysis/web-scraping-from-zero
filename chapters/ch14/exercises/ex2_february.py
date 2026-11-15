r"""Exercise 14.2 (medium).

    Collect the observations of London (`LON`) for February 2027, all pages, and print the number of days, the warmest maximum temperature and its date.

Expected output: chapters/ch14/expected/ex2_february.txt
Solution: chapters/ch14/solutions/ex2_february.py
"""
from urllib.parse import urljoin
import pandas as pd
import requests
BASE = "http://localhost:8000"
params = {"station": "LON", "start": "2027-02-01", "end": "2027-02-28"}

# Your code here
