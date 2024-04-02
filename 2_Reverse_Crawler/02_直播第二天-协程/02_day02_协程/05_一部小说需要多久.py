import requests
from lxml import etree
import time
import asyncio
import aiohttp
import aiofiles


def get_every_chapter_url(url):
    while 1:
        try:
            headers = {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
            }
            resp = requests.get(url, headers=headers, verify=False)  # verify=False
            tree = etree.HTML(resp.text)
            href_list = tree.xpath("//div[@class='booklist clearfix']/span/a/@href")
            # print(href_list)
            return href_list
        except:
            print("重来一次")
            time.sleep(3)


async def download_one(url):
    while 1:  # 我这里只是重试. 如果需要次数判断. 加上次数就可以了
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    page_source = await resp.text()
                    # 开始解析
                    tree = etree.HTML(page_source)
                    title = tree.xpath("//div[@class='chaptertitle clearfix']/h1/text()")[0].strip()
                    content = "\n".join(tree.xpath("//div[@id='BookText']/text()")).replace("\u3000", "")

                    async with aiofiles.open(f"./明朝那些事儿/{title}.txt", mode="w", encoding='utf-8') as f:
                        await f.write(content)
                    break
        except:
            print("报错了. 重试一下 ", url)

    print("下载完毕", url)


async def download(href_list):
    tasks = []
    for href in href_list:
        t = asyncio.create_task(download_one(href))
        tasks.append(t)
    await asyncio.wait(tasks)


def main():
    url = "https://www.zanghaihua.org/mingchaonaxieshier/"
    # 1. 拿到页面当中每一个章节的url
    href_list = get_every_chapter_url(url)
    # 2. 启动协程. 开始一节一节的下载
    asyncio.run(download(href_list)) # 运行起来协程任务


if __name__ == '__main__':
    main()
