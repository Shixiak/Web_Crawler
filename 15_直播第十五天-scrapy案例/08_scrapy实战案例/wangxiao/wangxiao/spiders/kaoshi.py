import scrapy
from scrapy.linkextractors import LinkExtractor
import json
from wangxiao.items import QuestionItem
from scrapy_redis.spiders import RedisSpider

class KaoshiSpider(scrapy.Spider):
    name = 'kaoshi'
    allowed_domains = ['wangxiao.cn']
    # redis_key = ""
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
                # url="http://ks.wangxiao.cn/exampoint/list?sign=jz1&subsign=7c8c594f50b968712051",
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
        points = resp.xpath("//ul[@class='section-point-item']")  # 1.这里有坑, 有些页面是直接怼在chapter-item里面的. 填坑
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
            # print(p_list, point_name)
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
        # print(resp.json())

        all_data = resp.json()
        data = all_data.get("Data")
        # 循环data
        all_questsions = []
        for ds in data:
            # 两种情况出现.
            questions = ds.get("questions")
            # questions 里面有东西
            if questions:
                # 把所有的题都放在一个列表里. 后面统一处理
                # 原来的写法
                # for q in questions:
                #     all_questsions.append(q)
                # 更加简单的写法
                all_questsions.extend(questions)
            else:  # questions 里面没东西, 题在materials -> 列表 -> questions,
                # 把所有的题都放在一个列表里. 后面统一处理
                materials = ds.get('materials')
                for m in materials:
                    qs = m.get("questions")
                    all_questsions.extend(qs)

        # 统一处理每一道题
        for q in all_questsions:
            content = q.get("content")
            text_analysis = q.get("textAnalysis")

            # 处理选项的问题
            opts = q.get('options')
            options = []
            right_options = []
            for opt in opts:
                # name.content
                # A.吃了
                name = opt.get("name")
                content = opt.get("content")
                xuanxaing = f"{name}.{content}"
                options.append(xuanxaing)

                is_right = opt.get("isRight")
                if is_right:
                    right_options.append(name)

            # options -> 每一个选项
            # 把选项添加到content中
            content += f"""
                <p>
                    {"<br/>".join(options)}
                </p>
            """.replace(" ", "").replace("\n", "")

            # right_options -> 正确的选项
            text_analysis = f"""
                <p>
                    {",".join(right_options)}
                </p>
            """ .replace(" ", "").replace("\n", "") + text_analysis

            item = QuestionItem()
            item['text_analysis'] = text_analysis.replace("<p>", "\n").replace("</p>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
            item['content'] = content.replace("<p>", "\n").replace("</p>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
            item['p_list'] = p_list
            item['p_name'] = p_name
            yield item
