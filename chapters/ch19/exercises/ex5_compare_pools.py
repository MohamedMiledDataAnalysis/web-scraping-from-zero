"""Exercise 19.5 (harder).

    Write `read_cover_pool(path)` that returns a dictionary with the issuer, the date and every field code. Copy the synthetic file twice under new names with `shutil.copy` (to imitate three issuers' files), read the three, and build a DataFrame with one row per file and the columns `issuer`, `M.1.1`, `M.2.2`.

Expected output: chapters/ch19/expected/ex5_compare_pools.txt
Solution: chapters/ch19/solutions/ex5_compare_pools.py
"""
import shutil
from pathlib import Path
import pandas as pd

# Your code here
