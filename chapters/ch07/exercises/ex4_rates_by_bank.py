"""Exercise 7.4 (harder).

    Print the average rate of each bank from the savings table, ignoring the missing rate, sorted from the highest. Use `rates.groupby("Bank")["Rate"].mean()`.

Expected output: chapters/ch07/expected/ex4_rates_by_bank.txt
Solution: chapters/ch07/solutions/ex4_rates_by_bank.py
"""
from io import StringIO
import pandas as pd
import requests

# Your code here
