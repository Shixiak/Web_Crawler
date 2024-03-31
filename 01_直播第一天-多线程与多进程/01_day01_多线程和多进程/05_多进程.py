from multiprocessing import Process
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def func(name):
    for i in range(1000):
        print(name, i)


if __name__ == '__main__':
    p1 = Process(target=func, args=("进程1",))
    p2 = Process(target=func, args=("进程2",))
    p1.start()
    p2.start()


# 多个任务极其雷同. 使用多线程
# 多个任务几乎无关联的情况用多进程
# 免费的IP代理池.
# 1. 去各大免费代理ip网站去抓取IP
# 2. 验证各个IP是否可用

