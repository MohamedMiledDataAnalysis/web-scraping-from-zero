"""Exercise 25.4 (harder).

    Draw one chart with the five watched products, each line divided by its own first price (so they all start at 1.0), and print which product ended the two weeks with the largest fall. Save it as `output/ch25/watchlist_index.png`.

Expected output: chapters/ch25/expected/ex4_index_chart.txt
Solution: chapters/ch25/solutions/ex4_index_chart.py
"""
import sqlite3
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt  # noqa: E402
change = (index.iloc[-1] - 1) * 100

# Your code here
