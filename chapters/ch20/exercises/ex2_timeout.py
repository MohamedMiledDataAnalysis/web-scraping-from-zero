r"""Exercise 20.2 (medium).

    Use `PoliteClient` with `timeout=1` and `tries=2` on `/trouble/slow?seconds=2`. Catch the error and print it.

Expected output: chapters/ch20/expected/ex2_timeout.txt
Solution: chapters/ch20/solutions/ex2_timeout.py
"""
import logging
import sys
sys.path.insert(0, ".")
from toolkit.polite import PoliteClient  # noqa: E402

# Your code here
