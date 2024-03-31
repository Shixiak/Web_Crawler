import scrapy


class HahahaSpider(scrapy.Spider):
    name = 'hahaha'
    allowed_domains = ['51job.com']
    start_urls = ['http://51job.com/']

    def parse(self, response):
        pass
