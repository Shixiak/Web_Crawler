import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import time

# csv: 逗号分隔内容的文件
# 周润发,李嘉诚,李佳琦,
f = open("data.csv", mode="w", encoding='utf-8')


def download_xinfadi(url):
    resp = requests.get(url)
    content = resp.text
    tree = etree.HTML(content)
    # tr_list = tree.xpath("//table[@class='hq_table']/tr")[1:]
    tr_list = tree.xpath("//table[@class='hq_table']/tr[position()>1]")
    for tr in tr_list:   # 每一行
        tds = tr.xpath("./td/text()")
        f.write(",".join(tds))
        f.write("\n")


if __name__ == '__main__':
    start = time.time()
    with ThreadPoolExecutor(30) as t:
        for i in range(1, 16):
            url = f"http://www.xinfadi.com.cn/marketanalysis/0/list/{i}.shtml"
            # download_xinfadi(url)
            t.submit(download_xinfadi, url)
    print("多线程用了", time.time() - start)
    start = time.time()
    for i in range(1, 16):
        url = f"http://www.xinfadi.com.cn/marketanalysis/0/list/{i}.shtml"
        download_xinfadi(url)
    print("单线程用了", time.time() - start)

    f.close()
