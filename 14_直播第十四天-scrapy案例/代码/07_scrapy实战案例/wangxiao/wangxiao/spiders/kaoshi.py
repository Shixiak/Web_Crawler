import scrapy
from scrapy.linkextractors import LinkExtractor
import json


class KaoshiSpider(scrapy.Spider):
    name = 'kaoshi'
    allowed_domains = ['wangxiao.cn']
    start_urls = ['http://ks.wangxiao.cn/']

    def parse(self, resp, **kwargs):
        le = LinkExtractor(restrict_xpaths="//ul[@class='first-title']/li/div/a")
        a_list = le.extract_links(resp)
        for a in a_list:
            first_title = a.text
            exampoint_url = a.url.replace("TestPaper", "exampoint")

            yield scrapy.Request(
                url=exampoint_url,
                callback=self.parse_second_level,
                meta={"first_title": first_title}  # 向后传递消息
            )
            break

    def parse_second_level(self, resp):
        first_title = resp.meta['first_title']
        le = LinkExtractor(restrict_xpaths="//div[@class='filter-content']/div[2]/a")
        a_list = le.extract_links(resp)
        for a in a_list:
            second_title = a.text
            # 准备进入第三层
            yield scrapy.Request(
                url=a.url,
                callback=self.parse_third_level,
                meta={"first_title": first_title, "second_title": second_title}
            )
            break

    def parse_third_level(self, resp):
        # print(resp.url)
        # print(resp.text)
        first_title = resp.meta['first_title']
        second_title = resp.meta['second_title']
        # 找到最里层的所有的点
        points = resp.xpath("//ul[@class='section-point-item']")
        for point in points:
            # 找到当前节点的所有父级节点. 到 :: 后结束
            parents = point.xpath("./ancestor-or-self::ul[@class='chapter-item' or @class='section-item']")

            p_list = [first_title, second_title]
            for p in parents:
                fu_name = "".join(p.xpath("./li[1]/text()").extract()).strip().replace(" ", "")
                p_list.append(fu_name)

            # 拿到了当前节点本身 + 父级目录结构
            # 一级建造师
            #   建设工程经济
            #       1Z101000工程经济
            #           1Z101010资金时间价值的计算及应用
            #               1Z101013名义利率与有效利率的计算
            #                   经济xxxxx.md   有文字. 有图片. 甚至还有视频..

            point_name = "".join(point.xpath("./li[1]/text()").extract()).strip().replace(" ", "")
            print(p_list, point_name)
            # 提取下个请求需要用到的三个参数
            point_count = point.xpath("./li[2]/text()").extract_first().split("/")[1]
            sign = point.xpath("./li[3]/span/@data_sign").extract_first()
            subsign = point.xpath("./li[3]/span/@data_subsign").extract_first()

            url = "http://ks.wangxiao.cn/practice/listQuestions"
            data = {
                "examPointType": "",
                "practiceType": "2",
                "questionType": "",
                "sign": sign,
                "subsign": subsign,
                "top": point_count,
            }

            yield scrapy.Request(  # post
                url=url,
                method="POST",
                body=json.dumps(data),  # request payload
                headers={
                    "X-Requested-With": "XMLHttpRequest",
                    "Content-Type": "application/json; charset=UTF-8"
                },
                callback=self.parse_point,
                meta={
                    "p_list": p_list,
                    "p_name": point_name
                }
            )
            break

    def parse_point(self, resp):
        p_list = resp.meta["p_list"]
        p_name = resp.meta["p_name"]
        print(resp.json())
        # 文件夹结构
        # 文件名
        # 拿到的所有的题
