import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import DropItem


class JobsSpider(scrapy.Spider):
    name = "jobs"
    start_urls = ["http://localhost:8000/jobs/"]

    def parse(self, response):
        for li in response.css("li.job"):
            yield {
                "id": li.attrib["data-id"],
                "title": li.css("h2.job-title a::text").get(),
                "city": li.css("p.location::text").get(),
                "salary": li.css("p.salary::text").get(),
            }
        next_page = response.css("ul.pager li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)


class CleanPipeline:
    def process_item(self, item, spider):
        low, high = item.pop("salary").split("–")
        item["salary_min"] = int(low.strip(" £").replace(",", ""))
        item["salary_max"] = int(high.strip(" £").replace(",", ""))
        item["id"] = int(item["id"])
        return item


class RemotePipeline:
    def process_item(self, item, spider):
        if item["city"] == "Remote":
            raise DropItem(f"remote job {item['id']}")
        return item


class CountPipeline:
    def open_spider(self, spider):
        self.count = 0

    def process_item(self, item, spider):
        self.count += 1
        return item

    def close_spider(self, spider):
        print(f"{self.count} jobs kept")


process = CrawlerProcess(settings={
    "ROBOTSTXT_OBEY": True,
    "USER_AGENT": "LearningScraper/1.0 (+mailto:reader@example.com)",
    "DOWNLOAD_DELAY": 0.2,
    "LOG_LEVEL": "ERROR",
    "ITEM_PIPELINES": {"__main__.CleanPipeline": 100,
                       "__main__.RemotePipeline": 200,
                       "__main__.CountPipeline": 300},
    "FEEDS": {"output/ch21/jobs.json": {"format": "json", "overwrite": True}},
})
process.crawl(JobsSpider)
process.start()

import json  # noqa: E402

jobs = json.load(open("output/ch21/jobs.json", encoding="utf-8"))
print(jobs[0])
print("Remote in file:", sum(j["city"] == "Remote" for j in jobs))
