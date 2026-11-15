import json

import scrapy
from scrapy.crawler import CrawlerProcess


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    start_urls = ["http://localhost:8000/quotes/"]

    def parse(self, response):
        for href in response.css("span.by a::attr(href)").getall():
            yield response.follow(href, self.parse_author)
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        yield {
            "name": response.css("h1.author-title::text").get(),
            "born": response.css("span.author-born-date::text").get(),
            "place": response.css(
                "span.author-born-location::text"
            ).get(),
        }


process = CrawlerProcess(
    settings={
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 0.2,
        "LOG_LEVEL": "ERROR",
        "USER_AGENT": "LearningScraper/1.0 (+mailto:reader@example.com)",
        "FEEDS": {
            "output/ch21/authors.json": {
                "format": "json",
                "overwrite": True,
            }
        },
    }
)
process.crawl(AuthorsSpider)
process.start()
authors = json.load(open("output/ch21/authors.json", encoding="utf-8"))
print(len(authors), "authors")
