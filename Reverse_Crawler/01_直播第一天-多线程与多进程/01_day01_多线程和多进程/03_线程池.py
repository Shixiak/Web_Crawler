from concurrent.futures import ThreadPoolExecutor
import time
import random
# def func(name):
#     for i in range(100):
#         print(name, i)
#
#
# if __name__ == '__main__':
#     with ThreadPoolExecutor(5) as t:
#         t.submit(func, "线程1")  # submit 提交
#         t.submit(func, "线程2")  # submit 提交
#         t.submit(func, "线程3")  # submit 提交
#         t.submit(func, "线程4")  # submit 提交
#         t.submit(func, "线程5")  # submit 提交
#         t.submit(func, "线程6")  # submit 提交
#         t.submit(func, "线程7")  # submit 提交
#         t.submit(func, "线程8")  # submit 提交
#         t.submit(func, "线程9")  # submit 提交


def func(name):
    # for i in range(100):
    #     print(name, i)
    time.sleep(random.randint(1,3))
    return name

def fn(res):
    print(res.result())  # 这种方案拿到的结果不是正常的顺序


if __name__ == '__main__':
    task_list = ["线程2", "线程3", "线程4", "线程5", "线程6"]
    with ThreadPoolExecutor(3) as t:
        # for task in task_list:
        #     t.submit(func, task).add_done_callback(fn)  # 直接提交任务
        result = t.map(func, task_list)  # 直接把一堆任务提交
        for r in result:
            print(r)
