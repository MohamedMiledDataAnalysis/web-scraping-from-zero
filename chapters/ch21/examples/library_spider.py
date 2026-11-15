import sys
from pathlib import Path

import scrapy

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "ch12" / "examples"))
from book_parser import parse_book_page  # noqa: E402


class LibrarySpider(scrapy.Spider):
    name = "library"
    start_urls = ["http://localhost:8000/library/"]
    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "USER_AGENT": "LearningScraper/1.0 (+mailto:reader@example.com)",
        "DOWNLOAD_DELAY": 0.2,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "LOG_LEVEL": "WARNING",
        "FEED_EXPORT_FIELDS": ["title", "author", "category", "price",
                               "rating", "stock", "pages", "year", "url"],
    }

    def parse(self, response):
        for href in response.css("article.book-card h3 a::attr(href)").getall():
            yield response.follow(href, self.parse_book)
        next_page = response.css("ul.pager li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_book(self, response):
        yield parse_book_page(response.url, response.text)
