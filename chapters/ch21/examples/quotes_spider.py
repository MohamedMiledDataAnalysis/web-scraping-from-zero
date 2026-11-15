import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["http://localhost:8000/quotes/"]
    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "USER_AGENT": "LearningScraper/1.0 (+mailto:reader@example.com)",
        "DOWNLOAD_DELAY": 0.2,
        "LOG_LEVEL": "WARNING",
    }

    def parse(self, response):
        for q in response.css("div.quote"):
            yield {
                "text": q.css("span.text::text").get().strip("“”"),
                "author": q.css("small.author::text").get(),
                "tags": q.css("a.tag::text").getall(),
            }
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
