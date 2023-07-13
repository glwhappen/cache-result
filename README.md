# Cache Function Result

## Description

这是一个Python包，它提供了一个装饰器用于缓存函数的返回结果。缓存的结果可以指定任意位置，非常的自由，缓存的键则是根据函数名、源代码和参数来控制的。你可以选择排除某些元素，例如函数名、源代码、参数或者关键字参数。

This is a Python package that provides a decorator for caching the results of functions. The cache is stored in a specified directory, and the cache key is generated based on the function name, source code, and arguments. The decorator allows you to exclude certain elements from the cache key, such as the function name, source code, arguments, or keyword arguments.


## Installation

You can install this package using pip:

```bash
pip install cache_result
```

## features

- 可以指定缓存的位置
- 可以自定义缓存的key，例如函数名、源代码、参数或者关键字参数
- 可以根据参数的名称指定不同的缓存文件夹


## Usage

Here is an example of how to use the cache decorator:

```python
from cache_result import cache

@cache('./cache/缓存/自己随便指定一些路径/方便自己区分/时间可以控制版本/20230713/add', exclude=['func_name'], is_print=True)
def add(a, b):
    # Your expensive function implementation here
    print("add", a, b)

    return a + b

print(add(1, 2))
print(add(1, 2))
```

## License

This project is licensed under the MIT License.

