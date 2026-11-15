"""Exercise 20.4 (harder).

    Write a log of a crawl of pages 1 to 3 of the library plus `/trouble/flaky` (after a reset) into `output/ch20/crawl.log`, with `PoliteClient` and a file handler. Then read the log file and print only the warning lines, without their time stamp.

Expected output: chapters/ch20/expected/ex4_log_file.txt
Solution: chapters/ch20/solutions/ex4_log_file.py
"""
import logging
import sys
from pathlib import Path
sys.path.insert(0, ".")
from toolkit.polite import PoliteClient  # noqa: E402

# Your code here
