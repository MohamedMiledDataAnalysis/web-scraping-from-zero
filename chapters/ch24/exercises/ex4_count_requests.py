"""Exercise 24.4 (harder).

    Count the requests the week sent: list pages and detail pages. Wrap `client.get` to count calls, run the week again quietly without emails, and print the totals.

Expected output: chapters/ch24/expected/ex4_count_requests.txt
Solution: chapters/ch24/solutions/ex4_count_requests.py
"""
import datetime as dt
import json
import logging
import sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, "chapters/ch24/project")
import tracker  # noqa: E402

# Your code here
