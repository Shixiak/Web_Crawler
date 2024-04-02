import asyncio
import time

#
# async def func1():
#     print("我是func1")
#     await asyncio.sleep(1)
#     print("func1结束")
#
#
# async def func2():
#     print("我是func2")
#     await asyncio.sleep(2)
#     print("func2结束")
#
#
# async def func3():
#     print("我是func3")
#     await asyncio.sleep(3)
#     print("func3结束")
#
#
# if __name__ == '__main__':
#     start = time.time()
#     f1 = func1()
#     f2 = func2()
#     f3 = func3()
#     # 把三个任务放一起
#     tasks = [
#         f1,
#         f2,
#         f3,
#     ]
#
#     asyncio.run(asyncio.wait(tasks))
#     print(time.time() - start)


async def download(url, t):
    print("我要下载了")
    await asyncio.sleep(t)
    print("我下载完了")


async def main():
    # 假设已经有了一堆下载链接
    urls = [
        "http://www.baidu.com",
        "http://luoyonghao.com",
        "http://qiaofuhaoshuai.com"
    ]
    # 需要封装任务列表
    tasks = []
    for url in urls:
        # 创建任务
        task = asyncio.create_task(download(url, 3))  # 加上这个就没有下面的警告了
        # 把任务扔到列表, 为了统一处理
        tasks.append(task)
    # 统一等到协程任务执行完毕
    await asyncio.wait(tasks)   # py3.8以上的同学. 回去这里会出现警告.


if __name__ == '__main__':
    asyncio.run(main())

    # event_loop = asyncio.get_event_loop()
    # event_loop.run_until_complete(main())
"""
未来爬虫:
    1. 扫url, 拿到一堆url
    2. 循环url. 创建任务. 
    3. 统一await
"""
