import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import DropItem


class JobsSpider(scrapy.Spider):
    name = "jobs"
    start_urls = ["http://localhost:8000/jobs/"]

    def parse(self, response):
        for li in response.css("li.job"):
            low, high = li.css("p.salary::text").get().split("–")
            yield {"title": li.css("h2.job-title a::text").get(),
                   "salary_max": int(high.strip(" £").replace(",", ""))}
        next_page = response.css("ul.pager li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)


class HighSalaryPipeline:
    def process_item(self, item, spider):
        if item["salary_max"] < 50000:
            raise DropItem("salary too low")
        return item


class CountPipeline:
    def open_spider(self, spider):
        self.count = 0

    def process_item(self, item, spider):
        self.count += 1
        return item

    def close_spider(self, spider):
        print(self.count, "jobs with a maximum salary of £50,000 or more")


process = CrawlerProcess(settings={
    "ROBOTSTXT_OBEY": True, "DOWNLOAD_DELAY": 0.2, "LOG_LEVEL": "ERROR",
    "USER_AGENT": "LearningScraper/1.0 (+mailto:reader@example.com)",
    "ITEM_PIPELINES": {"__main__.HighSalaryPipeline": 100,
                       "__main__.CountPipeline": 200}})
process.crawl(JobsSpider)
process.start()
