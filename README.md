# Cache Function Result

## Description

这是一个Python包，用于缓存函数的返回结果。缓存的结果持久化在本地。

This is a Python package that provides a decorator for caching the results of functions. The cache is stored in a specified directory, and the cache key is generated based on the function name, source code, and arguments. The decorator allows you to exclude certain elements from the cache key, such as the function name, source code, arguments, or keyword arguments.

## Use Case

- 你有一个计算密集型的函数，它需要花费很长时间来计算结果。你希望将结果缓存起来，以便下次使用时可以快速获取结果。
- 你有一个函数，它需要从网络上获取数据，但是获取的内容一般情况下不会改变，那么久可以缓存一下，如果改变了手动删除缓存即可。

## Installation

You can install this package using pip:

```bash
pip install cache_result
```

## features

- 可以自由指定缓存的位置，后续也可以随意的更改；
- 缓存的内容甚至可以发送给其他人，其他人也可以使用缓存的内容；
- 可以自定义缓存的key，例如函数名、源代码、参数或者关键字参数；
- 可以根据参数的名称指定不同的缓存文件夹；
- 缓存的key会根据源代码的变化而变化，但是如果修改了源代码中的输出，增加了空行或者空格，那么缓存的key不会发生变化；

## 参数说明

- `has_source_code`: 是否包含缓存函数的代码，默认 `false` 只会包含代码体，并且删除了代码中的输出注释的影响
- `is_print`: 是否输出缓存文件位置，默认为 `true`
- `exclude_args`: 排除一些参数，某些情况下不想让一些参数加入缓存，可以排除，默认为空
- `debug`: debug 模式，开启详细日志，默认为 `false`
- `hash_length`: 生成的文件长度，默认 `16`

## Usage

需要在根目录创建一个 `.projectroot` 文件，用来标识项目的根目录，这样缓存文件都会创建到根目录


缓存的计算斐波那契数列的第n项


```python
import time
from cache_result import cache

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

```

缓存路径可以随便写，方便自己区分

```python
import time
from cache_result import cache

@cache('./cache/缓存/自己随便指定一些路径/方便自己区分/时间可以控制版本/20230713/add', exclude=['func_name'], is_print=True)
def add(a, b):
    # Your expensive function implementation here
    print("add", a, b)
    time.sleep(3)

    return a + b

print(add(1, 2))
print(add(1, 2))
```

## License

This project is licensed under the MIT License.

