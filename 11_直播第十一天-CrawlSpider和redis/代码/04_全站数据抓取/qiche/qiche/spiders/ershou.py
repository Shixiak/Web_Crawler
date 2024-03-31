import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ErshouSpider(CrawlSpider):  # CrawlSpider也继承了Spider. 所以从根上讲. ErshouSpider依然是一个Spider
    name = 'ershou'
    allowed_domains = ['che168.com', 'autohome.com.cn']
    start_urls = ['https://www.che168.com/beijing/list/?pvareaid=100533']

    rules = (  # rule 规则, 这里定义了一堆规则. 要求必须是元组或者列表
        # Rule: 规则对象
        Rule(LinkExtractor(restrict_xpaths=("//ul[@class='viewlist_ul']/li/a",)), callback='parse_item', follow=False),
        Rule(LinkExtractor(restrict_xpaths=("//div[@id='listpagination']/a",)), follow=True),  # 根据需要.自由设定callback
    )

    # 这里不能自己写parse, parse由crawlSpider提供.
    def parse_item(self, resp):
        # 处理详情页
        title = resp.xpath("//div[@class='car-box']/h3/text()").extract_first()
        price = resp.xpath("//span[@id='overlayPrice']/text()").extract_first()
        print(title, price)

