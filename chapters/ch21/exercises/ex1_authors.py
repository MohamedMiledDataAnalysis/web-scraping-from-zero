r"""Exercise 21.1 (easy).

    Change `quotes_spider.py` to collect the author pages instead: from each quote, follow the *(about)* link and yield the name, birth year and birthplace. Scrapy's duplicate filter visits each author once. Print the number of authors in the file.

Expected output: chapters/ch21/expected/ex1_authors.txt
Solution: chapters/ch21/solutions/ex1_authors.py
"""
import json
import scrapy
from scrapy.crawler import CrawlerProcess

# Your code here
