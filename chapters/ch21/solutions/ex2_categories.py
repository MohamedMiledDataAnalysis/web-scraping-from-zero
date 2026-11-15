import pandas as pd
import scrapy
from scrapy.crawler import CrawlerProcess


class CategoriesSpider(scrapy.Spider):
    name = "categories"
    start_urls = ["http://localhost:8000/library/"]

    def parse(self, response):
        for a in response.css("aside.categories a"):
            yield response.follow(a, self.parse_category,
                                  cb_kwargs={"name": a.css("::text").get()})

    def parse_category(self, response, name):
        count = response.css("p.result-count strong::text").get()
        yield {"category": name, "books": int(count)}


process = CrawlerProcess(settings={
    "ROBOTSTXT_OBEY": True, "DOWNLOAD_DELAY": 0.2, "LOG_LEVEL": "ERROR",
    "USER_AGENT": "LearningScraper/1.0 (+mailto:reader@example.com)",
    "FEEDS": {"output/ch21/categories.csv": {"format": "csv", "overwrite": True}}})
process.crawl(CategoriesSpider)
process.start()
cats = pd.read_csv("output/ch21/categories.csv")
print(cats.sort_values(["books", "category"], ascending=[False, True]).head(3)
      .to_string(index=False))
