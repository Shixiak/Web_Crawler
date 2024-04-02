import asyncio


async def func1():
    print("我是func1")
    await asyncio.sleep(1)
    print("func1结束")
    return "func1的返回值"


async def func2():
    print("我是func2")
    await asyncio.sleep(2)
    print("func2结束")
    return "func2的返回值"


async def func3():
    print("我是func3")
    # print(1/0)  # 异常
    await asyncio.sleep(3)
    print("func3结束")
    return "func3的返回值"


async def main():
    f1 = func1()
    f2 = func2()
    f3 = func3()

    tasks = [
        asyncio.create_task(f3),
        asyncio.create_task(f2),  # 2 1 3      3 2 1
        asyncio.create_task(f1),
    ]

    # # 结束, 运行, set集合: 无序
    # # asyncio.wait() 返回的结果.没有顺序
    # done, pending = await asyncio.wait(tasks)
    # for t in done:
    #     print(t.result())

    # gather 和 wait的区别: gather返回值是有顺序(按照你添加任务的顺序返回的)的.
    # return_exceptions=True, 如果有错误信息. 返回错误信息, 其他任务正常执行.
    # return_exceptions=False, 如果有错误信息. 所有任务直接停止
    result = await asyncio.gather(*tasks, return_exceptions=True)  # return_exceptions=True
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
