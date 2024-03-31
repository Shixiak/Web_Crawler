"""

以下言论仅限今天的案例:

进程 1. 访问主页面, 在主页面中拿到详情页的url.
    进入到详情页. 在详情页中提取到图片的下载地址

进程 2. 批量的下载图片



进程之间的通信
队列

"""
import requests
from urllib import parse  # 转化
from lxml import etree
from multiprocessing import Process, Queue
from concurrent.futures import ThreadPoolExecutor


def get_img_src(q):
    url = "http://www.591mm.com/mntt/6.html"
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    # print(resp.text)
    tree = etree.HTML(resp.text)
    href_list = tree.xpath("//div[@class='MeinvTuPianBox']/ul/li/a[1]/@href")
    for href in href_list:
        # http://www.591mm.com/mntt/6.html
        # /mntt/hgmn/307626.html
        # 拼接url地址
        child_url = parse.urljoin(url, href)
        # print(child_url)
        resp_child = requests.get(child_url)
        resp_child.encoding = "utf-8"
        child_tree = etree.HTML(resp_child.text)
        src = child_tree.xpath("//img[@id='mouse_src']/@src")[0]
        q.put(src)  # 往里怼
    q.put("OK了")


def download(url):
    file_name = url.split("/")[-1]
    with open(file_name, mode="wb") as f:
        resp = requests.get(url)
        f.write(resp.content)  # 完成下载


def download_all(q):
    # 在进程里创建线程池
    with ThreadPoolExecutor(10) as t:
        while 1:
            src = q.get()  # 往出拿
            if src == "OK了":
                break
            print(src)
            t.submit(download, src)


if __name__ == '__main__':
    q = Queue()
    p1 = Process(target=get_img_src, args=(q,))
    p2 = Process(target=download_all, args=(q,))

    p1.start()
    p2.start()

