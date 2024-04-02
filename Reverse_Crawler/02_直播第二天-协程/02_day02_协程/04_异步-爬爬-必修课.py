# aiohttp, aiofiles
import asyncio
import aiohttp
import aiofiles




"""
"http://pic3.hn01.cn/wwl/upload/2021/05-30/lr53sysfkl5.jpg",
"http://pic3.hn01.cn/wwl/upload/2021/05-30/hgeuzfs4jt2.jpg",
"http://pic3.hn01.cn/wwl/upload/2021/05-30/kwpyey5xv2l.jpg",
"http://pic3.hn01.cn/wwl/upload/2021/05-30/w2xjeyllq1k.jpg",
"""


async def download(url):
    print("开始下载", url)
    file_name = url.split("/")[-1]
    # 相当于requests
    async with aiohttp.ClientSession() as session:
        # 发送网络请求
        async with session.get(url) as resp:
            # await resp.text()  # => resp.text
            content = await resp.content.read()  # => resp.content
            # 写入文件
            async with aiofiles.open(file_name, mode="wb") as f:
                await f.write(content)

    print("下载完成.", url)


async def main():
    url_list = [
        "http://pic3.hn01.cn/wwl/upload/2021/05-30/lr53sysfkl5.jpg",
        "http://pic3.hn01.cn/wwl/upload/2021/05-30/hgeuzfs4jt2.jpg",
        "http://pic3.hn01.cn/wwl/upload/2021/05-30/kwpyey5xv2l.jpg",
        "http://pic3.hn01.cn/wwl/upload/2021/05-30/w2xjeyllq1k.jpg",
    ]
    tasks = []
    for url in url_list:
        t = asyncio.create_task(download(url))
        tasks.append(t)

    await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.run(main())
