# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from lxml import etree
from scrapy import Request
import os  # 装着和操作系统相关的东西


class WangxiaoPipeline:

    def process_item(self, item, spider):
        # 没有图片的问题了
        # 剩下的就是写入的问题了
        content = item['content']
        text_analysis = item['text_analysis']

        p_list = item['p_list']
        p_name = item['p_name']

        # 关于文件夹路径的问题
        paths = os.path.join(*p_list)
        if not os.path.exists(paths):
            os.makedirs(paths)

        full_md_file_path = os.path.join(paths, f"{p_name}.md")

        with open(full_md_file_path, mode="a", encoding="utf-8") as f:
            f.write(content)
            f.write("\n")  # 文本的换行
            f.write(text_analysis)
            f.write("\n")
            f.write("------")  # md语法. 可以自动生成一个长长的横线
            f.write("\n")
        print("一道题处理完毕")
        return item


class WangxiaoImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):  # 发送请求.
        content = item['content']
        text_analysis = item['text_analysis']
        ct = etree.HTML(content)
        ta = etree.HTML(text_analysis)

        srcs = ct.xpath("//img/@src")
        srcs.extend(ta.xpath("//img/@src"))
        for src in srcs:
            # 可以开始下载图片了
            yield Request(
                url=src,
                meta={
                    "p_list": item['p_list'],
                    "p_name": item['p_name']
                }
            )

    def file_path(self, request, response=None, info=None):
        # 获取图片的存储路径
        # ['一级建造师',
        #     '建设工程经济',
        #         '1Z101000工程经济',
        #             '1Z101010资金时间价值的计算及应用',
        #                 '1Z101011利息的计算']
        #                     一、资金时间价值的概念.md     <img src="一、资金时间价值的概念_img/xxx.png">
        #                     一、资金时间价值的概念_img
        #                            xxx.png
        # 接收 目录结构, 文件名称_img
        img_name = request.url.split("/")[-1]
        p_list = request.meta['p_list']
        p_name = request.meta['p_name']
        img_path = os.path.join(*p_list, f"{p_name}_img")   # 一级建造师/建设工程/xxx/xxx/资金时间价值的概念_img
        return os.path.join(img_path, img_name)  # 一级建造师/建设工程/xxx/xxx/资金时间价值的概念_img/xxx.png

    def item_completed(self, results, item, info):
        # item_completed是在所有图片下载完毕之后. 才开始执行的
        # url 下载地址
        # img_path 完整路径   一级建造师/建设工程/xxx/xxx/资金时间价值的概念_img/xxx.png
        # 利用result里面的内容. 对item进行整改
        # [(True, {url:xxx, path:xxx}),(True, {url:xxx, path:xxx}),(True, {url:xxx, path:xxx})]
        for status, r in results:
            if status:
                img_url = r.get("url")
                img_path = r.get("path")  # 一级建造师/建设工程/xxx/xxx/资金时间价值的概念_img/xxx.png
                img_my_path = os.path.join(*img_path.split("/")[-2:])

                item['content'] = item['content'].replace(img_url, img_my_path)
                item['text_analysis'] = item['text_analysis'].replace(img_url, img_my_path)

        return item


"""
     {'content': '一定时间内等量资金的周转次数越多<img src="abc/hehe.png"/>，资金的时间价值越多<p>A.单位时间资金增值率一定的条件下、资金的时间价值与使用时间成正比<br/>B.资金随时间的推移而贬值的部分就是原有资金的时间价值<br/>C.投入资金总额一定的情况下，前期投入的资金越多，资金的正效益越大<br/>D.其他条件不变的情况下，资金的时间价值与资金数量成正比<br/>E.一定时间内等量资金的周转次数越多，资金的时间价值越多</p>',
     'p_list': ['一级建造师',
                '建设工程经济',
                '1Z101000工程经济',
                '1Z101010资金时间价值的计算及应用',
                '1Z101011利息的计算'],
     'p_name': '一、资金时间价值的概念',
     'text_analysis': '<p>A,D,E</ p><p>本题考查的是资金的时间的价值，C早收晚付。<br '
                      '/>（资金是时间函数，资金的价值随时间变化而变化的）<br '
                      '/></p><p>影响资金时间价值的因素很多，其中主要有以下几点：</p><p>1. '
                      '资金的使用时间。<img src="./d85bad94-21ed-467e-9675-e79e33b69ce5.png"/>在单位时间的资金增值率一定的条件下，资金<strong>使用时间越长，则资金的时间价值越大</strong>；使用时间越短，则资金的时间价值越小。</p><p>2. '
                      '资<strong>金数量的多少。在其他条件不变的情况下，资金数量越多，资金的时间价值就越多；反之，资金的时间价值则越少。</strong></p><p>3. '
                      '资金投入和回收的特点。在总资金一定的情况下，<strong>前期投入的资金越多，资金的负效益越大</strong>；反之，后期投入的资金越多，资金的负效益越小。而在资金回收额一定的情况下，离现在越近的时间回收的资金越多，资金的时间价值就越多；反之，离现在越远的时间回收的资金越多，资金的时间价值就越少。<br '
                      '/>4.资金周转的速度。资金周转越怏，在一定的时间内等量资金的<strong>周转次数越多，资金的时间价值越多</strong>；反之，资金的时间价值越少。<br '
                      '/>【知识点：资金时间价值的概念】【题库维护老师：ZCM】</p>'}


"""
