# Cache Function Result

[![Downloads](https://static.pepy.tech/badge/cache-result)](https://pepy.tech/project/cache-result)
[![Downloads](https://static.pepy.tech/badge/cache-result/month)](https://pepy.tech/project/cache-result)
[![Downloads](https://static.pepy.tech/badge/cache-result/week)](https://pepy.tech/project/cache-result)

## 描述

这个Python包专门设计用于缓存函数的返回结果，以便于将结果持久化并保存在本地。它能够基于函数的参数内容和代码变动来判定是否需要读取已有的缓存。

## 设计理念

- **持久性保障**：函数运行的结果将永久保存，除非用户主动删除缓存。
- **灵活分类存储**：缓存结果可以按重要程度存储在不同的子文件夹中，便于管理和控制。
- **手动控制更新**：若需要重新运行函数以获得最新结果，用户只需手动删除相应的缓存文件。

## 应用场景

- **加速计算处理**：对于耗时较长的计算密集型函数，可以通过缓存其结果，以便下次调用时能够迅速获取到。
- **稳定数据获取**：对于从网络获取数据的函数，如果获取的内容通常不会发生变化，可以通过缓存来保存结果。一旦数据有所改变，用户可以手动删除缓存以更新数据。
- **优化开发效率**：在开发大型语言模型时，可以通过缓存接口数据来节省成本并加快响应速度。

## 功能特点

- **灵活的缓存位置设置**：用户可以自由指定缓存保存的位置，并且随时更改位置设置。
- **共享缓存内容**：缓存的内容可以轻松分享给他人，使其他用户也能够利用已有的缓存数据。
- **按参数名称分类缓存**：可以根据不同的参数名称将缓存保存在不同的文件夹中，便于管理和检索。
- **时间驱动的缓存管理**：实现了基于时间的缓存控制，允许用户根据日期和时间来组织缓存文件，从而使得缓存管理更加高效和直观。这一特性特别适用于需要定期更新或具有时间敏感性的数据缓存。

## 安装指南

此包可通过pip进行安装：

```bash
pip install cache_result
```

## 快速使用

> 注意事项：需要在项目根目录创建一个 `.projectroot` 文件，用来标识项目的根目录，这样缓存文件都会创建到根目录

```python
import time

from cache_result import cache

@cache()
def add(a, b):
    time.sleep(4)
    return a + b

print("第一次运行需要花费4秒，再次运行只需要瞬间")
print(add(1, 2))
```


## 参数详解

- **代码包含设置** (`has_source_code`): 决定是否在缓存中包含函数的源代码。默认为 `false`，此时缓存将仅包含代码体，且忽略代码中的输出注释。
- **缓存位置提示** (`is_print`): 控制是否输出缓存文件的位置信息。默认设置为 `true`，便于用户了解缓存文件的存储位置。
- **参数排除选项** (`exclude_args`): 允许用户排除特定参数，避免某些参数被包含在缓存中。默认为空，即不排除任何参数。
- **调试模式** (`debug`): 启用此模式将开启详细的日志记录，方便调试和追踪问题。默认为 `false`。
- **哈希长度设置** (`hash_length`): 定义生成的缓存文件名的长度。默认长度为 `16`。



## 更多用法

> 注意事项：需要在项目根目录创建一个 `.projectroot` 文件，用来标识项目的根目录，这样缓存文件都会创建到根目录


### 分文件缓存

可以通过设置路径，添加不同的文件，并且文件的名称可以使用占位符

缓存的计算斐波那契数列的第n项，可以通过设置占位符，来让不同的结果缓存到不同的文件夹中。

```python
import time
from cache_result import cache

@cache('cache/fib/{n}')
def fib(n):
    """计算斐波那契数列的第n项"""
    if n < 2:
        return n
    else:
        return fib(n-1) + fib(n-2)

if __name__ == '__main__':
    print("计算斐波那契数列花费时间：")
    # 测试函数
    start = time.time()
    print(fib(40))  # 第一次计算将花费一些时间
    print('Time: ', time.time()-start)

    print("如果cache中有缓存结果了，再次运行会非常快")
    print("删除cache中的内容即可重新执行函数")
```

### 按时间缓存

如果需要按照时间让缓存失效，例如一天，一周，或者一小时

添加按时间缓存，允许根据日期和时间来组织缓存文件，从而使得缓存管理更加高效和直观。 完整的时间格式，可以自己控制：`{time:YYYY-MM-DD_HH-mm-ss}`

下面的写法是缓存一个小时

```python
import time

from cache_result import cache

@cache("cache/{time:YYYY-MM-DD_HH}")
def add(a, b):
    time.sleep(4)
    return a + b

print("第一次运行需要花费4秒，在一个小时内运行，只需要瞬间")
print(add(1, 2))
```

### 排除某些参数

如果输入的参数不会影响输出的结果，可以进行排除，这样他的改变不会导致重新计算缓存

```python
import time

from cache_result import cache

@cache("cache/{time:YYYY-MM-DD_HH}", exclude_args=['sleep'])
def add(a, b, sleep=4):
    time.sleep(sleep)
    return a + b

print("排除了sleep参数的影响，他的改变不会导致重新缓存")
print(add(1, 2))
print(add(1, 2, sleep=2))
```


## 高级用法

- 缓存目录的层级是方便用户区分的，缓存文件生成以后可以任意的修改缓存目录的层级，例如原来的缓存目录为 `cache/a` 可以直接改为 `cache/b` 然后把本地的缓存文件手动从 `a` 复制到 `b`

## License

This project is licensed under the MIT License.

