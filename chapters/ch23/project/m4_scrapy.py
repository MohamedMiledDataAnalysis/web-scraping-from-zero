"""Method 4: Chapter 21's Scrapy spider, with request statistics."""

import json
import sys
from pathlib import Path

import pandas as pd
from scrapy.crawler import CrawlerProcess

sys.path.insert(0, "chapters/ch21/examples")
from library_spider import LibrarySpider  # noqa: E402

OUT = Path("output/ch23")
process = CrawlerProcess(
    settings={
        "LOG_LEVEL": "ERROR",
        "FEEDS": {
            str(OUT / "m4_scrapy.csv"): {
                "format": "csv",
                "overwrite": True,
            }
        },
    }
)
crawler = process.create_crawler(LibrarySpider)
process.crawl(crawler)
process.start()
stats = crawler.stats.get_stats()
(OUT / "m4_meta.json").write_text(
    json.dumps({"requests": stats["downloader/request_count"]})
)
books = pd.read_csv(OUT / "m4_scrapy.csv")
print(
    len(books),
    "books,",
    stats["downloader/request_count"],
    "requests,",
    len(books.columns),
    "columns",
)
