r"""Exercise 21.2 (medium).

    Write a spider that collects, for every category of the library, its name and the number of books announced on its first page, and exports it to `output/ch21/categories.csv`. Print the three largest categories.

Expected output: chapters/ch21/expected/ex2_categories.txt
Solution: chapters/ch21/solutions/ex2_categories.py
"""
import pandas as pd
import scrapy
from scrapy.crawler import CrawlerProcess

# Your code here
