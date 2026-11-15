r"""Exercise 21.3 (medium).

    Add a pipeline to the jobs crawl that drops jobs whose maximum salary is under £50,000, and print how many jobs are kept.

Expected output: chapters/ch21/expected/ex3_salary_pipeline.txt
Solution: chapters/ch21/solutions/ex3_salary_pipeline.py
"""
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import DropItem

# Your code here
