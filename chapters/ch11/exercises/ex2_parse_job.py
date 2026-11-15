r"""Exercise 11.2 (medium).

    Write `parse_job_item(li)` for the items of the job board (`li.job`): `id` (from `data-id`, as a number), `title`, `company`, `city`, `salary_min`, `salary_max` (numbers), `posted`, and `new` (`True` if the item has the *New* badge). Print the first job of the board.

Expected output: chapters/ch11/expected/ex2_parse_job.txt
Solution: chapters/ch11/solutions/ex2_parse_job.py
"""
import requests
from bs4 import BeautifulSoup

# Your code here
