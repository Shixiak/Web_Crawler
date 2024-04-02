
from threading import Thread  # 线程

# # 1. 定义好. 线程要做哪些任务
# def func():
#     for i in range(1000):
#         print("子线程", i)
#
#
# # 2. 写main, 创建子线程
# if __name__ == '__main__':  # 要写这个
#     # t = Thread(target=func)  # 创建一个子线程, 该线程还没有被执行
#     # # 启动一个线程
#     # t.start()
#     # # 主线程继续执行下去.
#     # for i in range(1000):
#     #     print("主线程", i)
#     t1 = Thread(target=func)
#     t2 = Thread(target=func)
#     t1.start()
#     t2.start()


# def func(url):
#     # 编写爬虫的工作
#     print("我要编写爬虫的工作", url)
#
# if __name__ == '__main__':
#     urls = ["第一个", "第二个", "第三个"]
#     for u in urls:
#         # 注意, 线程不是创建的越多就越好. CPU核心数 * 4
#         t = Thread(target=func, args=(u, ))  # args可以给线程传递参数. 但是必须是元组.
#         t.start()


#
# class MyThread(Thread):  # 自己定义一个类. 继承Thread
#
#     def __init__(self, name):
#         super(MyThread, self).__init__()
#         self.name = name
#
#     def run(self):  # 固定的.  # 必须要编写run方法
#         for i in range(1000):
#             print(self.name, i)
#
#
# if __name__ == '__main__':
#     t1 = MyThread("线程1")
#     t2 = MyThread("线程2")
#
#     t1.start()
#     t2.start()


