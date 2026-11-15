r"""Exercise 4.1 (easy).

    Print the host, the path and the value of `q` in `http://localhost:8000/jobs/?q=python&city=London`.

Expected output: chapters/ch04/expected/ex1_parse_url.txt
Solution: chapters/ch04/solutions/ex1_parse_url.py
"""
from urllib.parse import urlparse, parse_qs

# Your code here
