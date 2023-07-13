import time

from cache_result import cache


# def fib(a):
#     return fib(a + 1) + fib(a + 2)

# 使用装饰器
@cache('./cache/缓存/自己随便指定一些路径/方便自己区分/时间可以控制版本/20230713/add', is_print=True)
def add(a, b):
    # Your expensive function implementation here
    print("add", a, b)

    time.sleep(3)

    return a + b

print(add(1, 2))
print(add(1, 2))
print(add(1, 3))
print(add(1, 2))