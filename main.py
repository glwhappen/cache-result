import time

from cache_result import cache


# def fib(a):
#     return fib(a + 1) + fib(a + 2)

# 使用装饰器
@cache('./cache/缓存/自己随便指定一些路径/方便自己区分/时间可以控制版本/20230713/add/{a}/{b}', is_print=True)
def add(a, b):
    # Your expensive function implementation here
    print("add", a, b)

    time.sleep(3)

    return a + b

@cache('./cache/fib/{n}')
def fib(n):
    """计算斐波那契数列的第n项"""
    if n < 2:
        return n
    else:
        return fib(n-1) + fib(n-2)


if __name__ == '__main__':
    print("斐波那契数列缓存测试")
    # 测试函数
    start = time.time()
    print(fib(30))  # 第一次计算将花费一些时间
    print('斐波那契数列 计算 - Time taken: ', time.time()-start)

    start = time.time()
    print(fib(30))  # 第二次运行将从缓存中获取结果，所以会很快
    print('斐波那契数列 读缓存 - Time taken: ', time.time()-start)

    print("加法缓存测试")
    start = time.time()
    print(add(1, 2))  # 第一次计算将花费一些时间
    print('加法 计算 - Time taken: ', time.time()-start)

    start = time.time()
    print(add(1, 2))  # 第二次运行将从缓存中获取结果，所以会很快
    print('加法 读缓存 - Time taken: ', time.time()-start)