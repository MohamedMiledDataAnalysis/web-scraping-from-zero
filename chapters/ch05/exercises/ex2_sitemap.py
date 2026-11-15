"""Exercise 5.2 (easy).

    Print the address of the sitemap announced in `robots.txt`, using the parser's `site_maps()` method, then print how many addresses the sitemap lists (count the `<loc>` tags).

Expected output: chapters/ch05/expected/ex2_sitemap.txt
Solution: chapters/ch05/solutions/ex2_sitemap.py
"""
from urllib.robotparser import RobotFileParser
import requests
from bs4 import BeautifulSoup

# Your code here
