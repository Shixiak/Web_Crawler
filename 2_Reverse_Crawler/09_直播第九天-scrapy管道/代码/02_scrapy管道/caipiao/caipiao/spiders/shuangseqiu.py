import scrapy
from caipiao.items import CaipiaoItem  # 先导包


class ShuangseqiuSpider(scrapy.Spider):
    name = 'shuangseqiu'
    allowed_domains = ['500.com']
    start_urls = ['http://datachart.500.com/ssq/']

    def parse(self, resp, **kwargs):
        # result = []
        trs = resp.xpath("//tbody[@id='tdata']/tr")
        for tr in trs:
            if tr.xpath("./@class").extract_first() == 'tdbck':
                continue
            # red_ball = tr.xpath("./td[@class='chartBall01']/text()").extract()
            # scrapy支持xpath和css混着用
            red_ball = tr.css(".chartBall01::text").extract()
            blue_ball = tr.css(".chartBall02::text").extract_first()
            qihao = tr.xpath("./td[1]/text()").extract_first().strip()

            cai = CaipiaoItem()  # cai = dict()
            cai['qihao'] = qihao
            cai['red_ball'] = red_ball
            cai['blue_ball'] = blue_ball
            yield cai  # 聪明人都这么干

            # dic = {
            #     "qihao": qihao,
            #     "red_ball": red_ball,
            #     "blue_ball": blue_ball,
            # }
            # # result.append(dic)
            # yield dic  # 别这么干, 很傻
        # return result  别这么干.很傻
        # yield result 别这么干, 很傻



