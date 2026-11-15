r"""Exercise 22.1 (easy).

    Using `history.py`, store the jobs of 1 and 10 March 2027 in a new database `output/ch22/ex1.db`, and print the number of new and removed jobs on the 10th.

Expected output: chapters/ch22/expected/ex1_two_days.txt
Solution: chapters/ch22/solutions/ex1_two_days.py
"""
import logging
import sys
from pathlib import Path
sys.path.insert(0, "chapters/ch22/examples")
import daily_jobs  # noqa: E402
from history import compare, save_day  # noqa: E402
db = "output/ch22/ex1.db"

# Your code here
