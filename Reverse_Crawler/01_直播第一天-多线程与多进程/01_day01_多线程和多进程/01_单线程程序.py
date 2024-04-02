
def func():
    for i in range(100):
        print("函数内", i)


if __name__ == '__main__':  # 程序的入口
    for i in range(100):
        print("函数外", i)
    func()
