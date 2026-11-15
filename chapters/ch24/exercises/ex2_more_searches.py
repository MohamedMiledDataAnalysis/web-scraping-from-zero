"""Exercise 24.2 (medium).

    Add `"sql"` to the searches of a copy of the configuration and count, without storing anything, how many matching jobs the board has on 2027-03-07 with and without it. Use `collect_list` and `matches`.

Expected output: chapters/ch24/expected/ex2_more_searches.txt
Solution: chapters/ch24/solutions/ex2_more_searches.py
"""
import json
import logging
import sys
from pathlib import Path
sys.path.insert(0, "chapters/ch24/project")
from tracker import collect_list, matches  # noqa: E402

# Your code here
