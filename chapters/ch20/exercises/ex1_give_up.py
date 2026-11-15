r"""Exercise 20.1 (easy).

    Use `get_with_retries` from `backoff.py` (copy the function) on `/trouble/status/500` with 3 tries and `base_wait=0.2`, and catch the final error to print its message.

Expected output: chapters/ch20/expected/ex1_give_up.txt
Solution: chapters/ch20/solutions/ex1_give_up.py
"""
import time
import requests
RETRY_STATUS = {429, 500, 502, 503, 504}

# Your code here
