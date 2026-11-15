import subprocess
import sys

code = r'''
import sys
sys.path.insert(0, "chapters/ch21/examples")
from scrapy.crawler import CrawlerProcess
from library_spider import LibrarySpider
process = CrawlerProcess(settings={
    "CLOSESPIDER_ITEMCOUNT": 30, "HTTPCACHE_ENABLED": True,
    "HTTPCACHE_DIR": "output/ch21/httpcache", "LOG_LEVEL": "ERROR",
    "FEEDS": {"output/ch21/first30.json": {"format": "json", "overwrite": True}}})
crawler = process.create_crawler(LibrarySpider)
process.crawl(crawler)
process.start()
stats = crawler.stats.get_stats()
print(stats.get("item_scraped_count", 0) >= 30, "| from cache:",
      stats.get("httpcache/hit", 0) > 0)
'''
import shutil  # noqa: E402

shutil.rmtree("output/ch21/httpcache", ignore_errors=True)
for run in [1, 2]:
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    print("Run", run, "- at least 30 items:", result.stdout.strip())
