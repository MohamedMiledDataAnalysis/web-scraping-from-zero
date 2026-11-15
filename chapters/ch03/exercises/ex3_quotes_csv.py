r"""Exercise 3.3 (medium).

    Save the list of three quotes given in the starter file to `output/ch03/quotes.csv` with the columns `author` and `text`, then read the file back and print the number of rows and the author of the last one.

Expected output: chapters/ch03/expected/ex3_quotes_csv.txt
Solution: chapters/ch03/solutions/ex3_quotes_csv.py
"""
import csv
from pathlib import Path
quotes = [
    {
        "author": "Ada Fernhill",
        "text": "Small daily efforts build tall houses.",
    },
    {
        "author": "Walter Pike",
        "text": "Measure the wood, not your worries.",
    },
    {
        "author": "June Albright",
        "text": "Start the day with one good sentence.",
    },
]

# Your code here
