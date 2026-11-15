"""Exercise 18.3 (medium).

    Log in with `requests`, download `orders.csv` into `output/ch18/orders.csv`, read it with pandas, and print the total of all orders and the orders still *On its way*.

Expected output: chapters/ch18/expected/ex3_orders_csv.txt
Solution: chapters/ch18/solutions/ex3_orders_csv.py
"""
from pathlib import Path
import pandas as pd
import requests
from bs4 import BeautifulSoup
BASE = "http://localhost:8000"

# Your code here
