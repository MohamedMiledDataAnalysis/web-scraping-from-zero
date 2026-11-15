r"""Exercise 20.3 (medium).

    Scrape pages 1 to 5 of the library with `PoliteClient`, build a DataFrame of titles and prices, and run `check_books` on it with `expected_rows=100`. Then run the same check on a version where you break the price selector on purpose.

Expected output: chapters/ch20/expected/ex3_checks.txt
Solution: chapters/ch20/solutions/ex3_checks.py
"""
import sys
import pandas as pd
from bs4 import BeautifulSoup
sys.path.insert(0, ".")
sys.path.insert(0, "chapters/ch20/examples")
from checks import check_books  # noqa: E402
from toolkit.polite import PoliteClient  # noqa: E402

# Your code here
