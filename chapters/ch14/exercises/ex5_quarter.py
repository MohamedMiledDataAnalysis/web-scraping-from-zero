r"""Exercise 14.5 (harder).

    For each of the five stations, collect the observations of the first quarter of 2027 (1 January to 31 March, 9 pages per station: 45 requests), respecting the limit with `api_get`. Print the total rainfall of each station, highest first, and the number of 429 answers you received.

Expected output: chapters/ch14/expected/ex5_quarter.txt
Solution: chapters/ch14/solutions/ex5_quarter.py
"""
import time
from urllib.parse import urljoin
import pandas as pd
import requests
BASE = "http://localhost:8000"
limited = 0

# Your code here
