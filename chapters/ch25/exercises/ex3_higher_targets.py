r"""Exercise 25.3 (medium).

    Run the alerts of 2027-03-10 again with a target 5% higher for every product, without collecting again (`alerts_for` reads the database only).

Expected output: chapters/ch25/expected/ex3_higher_targets.txt
Solution: chapters/ch25/solutions/ex3_higher_targets.py
"""
import sys
import pandas as pd
sys.path.insert(0, "chapters/ch25/project")
from monitor import alerts_for  # noqa: E402

# Your code here
