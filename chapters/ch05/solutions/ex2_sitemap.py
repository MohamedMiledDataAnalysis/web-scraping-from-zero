from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

robots = RobotFileParser("http://localhost:8000/robots.txt")
robots.read()
sitemap_url = robots.site_maps()[0]
print(sitemap_url)
xml = requests.get(sitemap_url, timeout=10).text
soup = BeautifulSoup(xml, "html.parser")
print(len(soup.find_all("loc")), "addresses")
