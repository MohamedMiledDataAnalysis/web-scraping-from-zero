"""Exercise 21.4 (harder).

    Run the library spider with `CLOSESPIDER_ITEMCOUNT` set to 30 and `HTTPCACHE_ENABLED` set to `True`, twice, and print the number of items each time and whether the second run sent requests to the site. Use the `httpcache/hit` statistic of the crawler's stats.

Expected output: chapters/ch21/expected/ex4_cache.txt
Solution: chapters/ch21/solutions/ex4_cache.py
"""
import subprocess
import sys
import sys
sys.path.insert(0, "chapters/ch21/examples")
from scrapy.crawler import CrawlerProcess
from library_spider import LibrarySpider
import shutil  # noqa: E402

# Your code here
