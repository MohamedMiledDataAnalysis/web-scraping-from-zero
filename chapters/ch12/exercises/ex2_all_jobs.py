"""Exercise 12.2 (medium).

    Collect every job of the job board on the site date (all pages; the *next* link is in `ul.pager li.next a`). Print the number of jobs and the three cities with the most jobs.

Expected output: chapters/ch12/expected/ex2_all_jobs.txt
Solution: chapters/ch12/solutions/ex2_all_jobs.py
"""
import time
from collections import Counter
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# Your code here
