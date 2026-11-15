r"""Exercise 13.4 (medium).

    Scrape pages 1 and 2 of the library twice each (four requests), build a DataFrame, and show that it has 80 rows but only 40 distinct books. Save the clean 40 to `output/ch13/books_p1_p2.csv`.

Expected output: chapters/ch13/expected/ex4_dedupe.txt
Solution: chapters/ch13/solutions/ex4_dedupe.py
"""
from pathlib import Path
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Your code here
