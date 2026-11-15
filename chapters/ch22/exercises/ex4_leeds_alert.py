r"""Exercise 22.4 (harder).

    Write an alert that sends an email only when a **Leeds** job with a maximum salary of at least £60,000 appears between 2027-03-05 and 2027-03-06, using the test mailbox. Print the email's subject line, or `No alert` if nothing qualifies.

Expected output: chapters/ch22/expected/ex4_leeds_alert.txt
Solution: chapters/ch22/solutions/ex4_leeds_alert.py
"""
import logging
import sys
from pathlib import Path
sys.path.insert(0, ".")
sys.path.insert(0, "chapters/ch22/examples")
from alert import send_alert  # noqa: E402
from daily_jobs import run  # noqa: E402
from toolkit.mailbox import start_test_mailbox  # noqa: E402

# Your code here
