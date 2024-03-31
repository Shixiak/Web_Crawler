"""
1. 一般情况下. 一个网页里想要显示出一个视频资源. <video>
2. 几乎没有视频网站会在video中直接给出视频的地址
    #                                  1G 2G 4G
    # <video src="http://www.baidu.com/苍老师.MP4"></video>
    # 用户体验极差. 占网速, 占内存
    # 切片
    =  abc.ts
    =  efg.ts
    =  123.ts
    # 必须把ts文件的正确顺序进行保存 -> M3U文件 -> utf-8 -> M3U8文件
3. 正确的视频加载过程:
    1. 先请求到M3U8文件
    2. 加载ts文件
    3. 正常播放视频资源
    服务器压力小. 用户体验好.
"""

# 针对网吧电影的分析:
# 1. 拿到视频页的页面源代码.
# 2. 从视频页的页面源代码中找到对应的iframe, 提取到iframe里面的src
# 3. 请求到src对应的页面源代码. 在该页面中解析出真正的M3U8文件地址
# 4. 下载第一层M3U8. 从第一层M3U8中解析出第二层的地址
# 5. 下载第二层M3U8. 从第二层M3U8中解析出每一个TS文件的路径, 启动协程任务
# 6. 对ts文件进行解密操作: 先拿key
# 7. 对ts文件进行合并. 还原回mp4文件

import requests
from lxml import etree
from urllib import parse
import re
import asyncio
import aiohttp
import aiofiles
from Crypto.Cipher import AES  # pip install pycryptodome
import os  # 用它来执行操作系统的命令


def get_page_source(url):
    resp = requests.get(url)
    return resp.text


def get_iframe_src(url):
    print("获取iframe的src值")
    # 1. 拿到视频页的页面源代码.
    page_source = get_page_source(url)
    # 2. 从视频页的页面源代码中找到对应的iframe, 提取到iframe里面的src
    tree = etree.HTML(page_source)
    src = tree.xpath("//iframe/@src")[0]
    # /js/player/?url=https://video.buycar5.cn/20200824/1EcQQ5Ww/index.m3u8&id=30288&num=1&count=1&vt=1
    src_url = parse.urljoin(url, src)
    print("成功获取iframe的src值", src_url)
    return src_url


def get_first_m3u8_url(src_url):
    print("获取第一层M3U8地址")
    page_source = get_page_source(src_url)
    # 在js里提取数据. 最好用的方案: re
    obj = re.compile(r'url: "(?P<m3u8_url>.*?)",', re.S)
    result = obj.search(page_source)
    m3u8_url = result.group("m3u8_url")
    print("成功获取到第一层M3U8地址")
    return m3u8_url


def download_m3u8_file(first_m3u8_url):
    print("下载第二层M3U8地址")
    # 获取到第二层M3U8文件, 并保存在硬盘中
    first_m3u8 = get_page_source(first_m3u8_url)
    second_m3u8_url = first_m3u8.split()[-1]
    second_m3u8_url = parse.urljoin(first_m3u8_url, second_m3u8_url)

    # 下载第二层M3U8文件
    second_m3u8 = get_page_source(second_m3u8_url)
    with open("second_m3u8.txt", mode='w', encoding='utf-8') as f:
        f.write(second_m3u8)
    print("下载第二层M3U8成功....数据以保存在second_m3u8.txt 文件中....")


async def download_one(url):  # url: ts文件的下载路径
    # 自省
    for i in range(10):
        try:
            file_name = url.split("/")[-1]
            async with aiohttp.ClientSession() as session:  # requests, requests.session()
                async with session.get(url, timeout=90) as resp:
                    content = await resp.content.read()
                    async with aiofiles.open(f"./电影_源_加密后/{file_name}", mode="wb") as f:
                        await f.write(content)
            print(url, "下载成功")
            break
        except:
            print("下载失败, 出现错误", url)
            # time.sleep() # 可以适当的进行睡眠
            # 异步爬虫没必要
            await asyncio.sleep((i+1) * 5)


async def download_all_ts():
    tasks = []
    with open("second_m3u8.txt", mode="r", encoding='utf-8') as f:
        for line in f:
            if line.startswith("#"):
                continue
            line = line.strip()  # 必须处理
            task = asyncio.create_task(download_one(line))
            tasks.append(task)
    await asyncio.wait(tasks)


def get_key():
    obj = re.compile(r'URI="(?P<key_url>.*?)"')
    key_url = ""
    with open("second_m3u8.txt", mode="r", encoding='utf-8') as f:
        result = obj.search(f.read())
        key_url = result.group("key_url")
    # 请求到key的url, 获取到真正的秘钥
    key_str = get_page_source(key_url)
    return key_str.encode('utf-8')


async def des_one(file, key):
    print("即将开始解密", file)
    # 加密解密对象创建
    aes = AES.new(key=key, IV=b"0000000000000000", mode=AES.MODE_CBC)
    async with aiofiles.open(f"./电影_源_加密后/{file}", mode="rb") as f1, \
            aiofiles.open(f"./电影_源_解密后/{file}", mode="wb") as f2:
        # 从加密后的文件中读取出来. 进行解密. 保存在未加密文件中
        content = await f1.read()
        bs = aes.decrypt(content)
        await f2.write(bs)
    print("文件已经解密", file)


async def des_all_ts_file(key):
    tasks = []
    with open("second_m3u8.txt", mode="r", encoding='utf-8') as f:
        for line in f:
            if line.startswith("#"):
                continue
            line = line.strip()
            file_name = line.split("/")[-1]
            # 准备异步操作
            task = asyncio.create_task(des_one(file_name, key))
            tasks.append(task)

    await asyncio.wait(tasks)


def merge_ts():
    name_list = []
    with open("second_m3u8.txt", mode="r", encoding='utf-8') as f:
        for line in f:
            if line.startswith("#"):
                continue
            line = line.strip()
            file_name = line.split("/")[-1]
            name_list.append(file_name)
    # print(name_list)
    # 切换工作目录 到 ./电影_源_解密后/
    # 1.记录当前工作目录
    now_dir = os.getcwd()
    print(now_dir)
    # 2. 切换工作目录 到 ./电影_源_解密后/
    os.chdir("./电影_源_解密后/")
    # 分而治之
    # 一次性合并100个文件
    temp = []
    n = 1
    for i in range(len(name_list)):
        name = name_list[i]
        temp.append(name)  # [a.ts, b.ts, c.ts]
        if i != 0 and i % 100 == 0:  # 每100个合并一次
            # 合并,
            # cat a.ts b.ts c.ts > xxx.mp4
            # copy /b a.ts + b.ts + c.ts xxx.mp4
            names = " ".join(temp)
            os.system(f"cat {names} > {n}.ts")
            n += 1
            temp = []  # 还原成新的待合并列表
    # 把最后没有合并的进行收尾
    names = " ".join(temp)
    os.system(f"cat {names} > {n}.ts")
    n += 1

    temp_2 = []
    # 把所有的n进行循环
    for i in range(1, n):
        temp_2.append(f"{i}.ts")

    names = " ".join(temp_2)
    os.system(f"cat {names} > movie.mp4")

    # 3. 所有的操作之后. 一定要把工作目录切换回来
    os.chdir(now_dir)


def main():
    url = "http://www.wbdy.tv/play/30288_1_1.html"
    src_url = get_iframe_src(url)
    # 3.访问src_url. 提取到第一层m3u8文件地址
    first_m3u8_url = get_first_m3u8_url(src_url)
    download_m3u8_file(first_m3u8_url)

    asyncio.run(download_all_ts())

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(download_all_ts())

    # 进行解密
    key = get_key()
    asyncio.run(des_all_ts_file(key))

    # 合并ts文件
    merge_ts()


if __name__ == '__main__':
    # main()
    # n = 0
    # with open("second_m3u8.txt", mode="r", encoding='utf-8') as f:
    #     for line in f:
    #         if line.startswith("#EXTINF:"):
    #             line = line.strip()
    #             line = line.strip(",")
    #             n += float(line.split(":")[-1])
    n = 7587

    print(n/60)
    print(126.45%60)