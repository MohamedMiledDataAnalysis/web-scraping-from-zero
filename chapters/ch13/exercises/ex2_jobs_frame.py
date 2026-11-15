"""Exercise 13.2 (medium).

    Scrape the job board (page 1 only), build a DataFrame with `title`, `city`, `salary` (the text) and `posted` (from the `datetime` attribute), then add the columns `salary_min`, `salary_max` (integers, with a regular expression) and `age_days` (days between `posted` and 2027-03-01). Print the three newest jobs.

Expected output: chapters/ch13/expected/ex2_jobs_frame.txt
Solution: chapters/ch13/solutions/ex2_jobs_frame.py
"""
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
rows = [{"title": li.select_one("h2 a").text,
         "city": li.select_one("p.location").text,
         "salary": li.select_one("p.salary").text,
         "posted": li.select_one("p.posted time")["datetime"]}
        for li in soup.select("li.job")]

# Your code here
