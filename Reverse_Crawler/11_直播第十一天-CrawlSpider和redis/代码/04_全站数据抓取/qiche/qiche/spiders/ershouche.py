import scrapy
from scrapy.linkextractors import LinkExtractor  # 链接提取器


class ErshoucheSpider(scrapy.Spider):
    name = 'ershouche'
    allowed_domains = ['chhttps://www.che168.com/beijing/list/?pvareaid=100533e168.com', 'autohome.com.cn']
    start_urls = ['']

    def parse(self, resp, **kwargs):
        # hrefs = resp.xpath("//ul[@class='viewlist_ul']/li/a/@href").extract()
        # for href in hrefs:
        #     yield scrapy.Request(
        #         url=resp.urljoin(href),
        #         callback=self.parse_detail
        #     )
        # scrapy 还提供了链接提取器的东西. 也可以帮我们提取到页面中的超链接
        le = LinkExtractor(restrict_xpaths=("//ul[@class='viewlist_ul']/li/a",))
        links = le.extract_links(resp)  # 提取链接
        # print(links)
        for link in links:
            # print(link.text.replace(" ", "").strip(), link.url)
            yield scrapy.Request(
                url=link.url,
                callback=self.parse_detail
            )

        # 开始分页
        print(resp.url)
        page_le = LinkExtractor(restrict_xpaths=("//div[@id='listpagination']/a",))
        page_links = page_le.extract_links(resp)   # 提取分页url
        for page in page_links:

            yield scrapy.Request(
                url=page.url,  # 重复的url没关系. scrapy自动的帮我们完成去除重复
                # dont_filter=True,  # 不过滤 - 直接扔队列  别乱加
                callback=self.parse  # 下一页的内容和当前页一致. 然后数据解析的过程和当前页一制
            )

    def parse_detail(self, resp, **kwargs):
        pass
