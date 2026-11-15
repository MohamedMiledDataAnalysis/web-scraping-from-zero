r"""Exercise 8.4 (harder).

    Write a function `fetch(session, url)` that returns the text of a page, or `None` after printing a short message when the request times out or the status is an error. Test it on `/library/`, `/trouble/slow?seconds=5` (with `timeout=2`) and `/trouble/status/404`.

Expected output: chapters/ch08/expected/ex4_fetch.txt
Solution: chapters/ch08/solutions/ex4_fetch.py
"""
import requests

# Your code here
