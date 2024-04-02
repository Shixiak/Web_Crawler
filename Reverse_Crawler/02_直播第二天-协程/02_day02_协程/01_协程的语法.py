import asyncio


"""
该函数执行时得到的是一个协程对象. 
"""
async def func():
    print("我是函数")


if __name__ == '__main__':  # 程序的入口
    # 协程对象想要执行. 必须借助于 event_loop
    # f = func()
    # print(f)

    f = func()  # 协程对象想要执行. 必须借助于 event_loop
    # # 拿到事件循环
    # event_loop = asyncio.get_event_loop()
    # # eventloop执行协程对象. 直到该对象内的内容执行完毕为止.
    # event_loop.run_until_complete(f)

    asyncio.run(f)
    # 如果你的电脑报错: Event Loop has closed!!!  
