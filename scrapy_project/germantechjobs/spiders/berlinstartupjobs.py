import scrapy
from germantechjobs.items import JobsStartup

class ItSoftwareSpider(scrapy.Spider):
    name = "berlinstartupjobs"
    
    def start_requests(self):
        urls = [
            "https://berlinstartupjobs.com/engineering/",
            "https://berlinstartupjobs.com/engineering/page/2/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        jobs = response.xpath("//li[contains(@class, 'bjs-jlid') and position() >= 1 and position() <= 25]")

        for job in jobs:
            a_links = job.xpath(".//h4[@class='bjs-jlid__h']/a/@href").get()
            if a_links:
                yield response.follow(a_links, callback=self.parse_post)

    def parse_post(self, response):
        # this is because sometimes the email is not found, so the code tries another selector
        apply_for_this_job = response.xpath("//*[@id='content']/div[2]/div[1]/div/div[1]/div[3]/div[1]/p/a/@href").get()
        if apply_for_this_job is None:
            apply_for_this_job = response.xpath("//*[@id='content']/div[2]/div[1]/div/div[1]/div[3]/a/@href").get()

        item = JobsStartup(
            title = response.xpath("//h1[@class='title']/text()").get(),
            tags = response.xpath("//a[@class='bsj-tag']/text()").getall() or None,
            company = response.xpath("normalize-space(//*[@id='content']/div[2]/div[1]/div/div[2]/div/div[1]/div/header/div/h2/a/text())").get(),
            apply_for_this_job = apply_for_this_job,
            location = "Berlin",
            url = response.url
        )
        yield item
