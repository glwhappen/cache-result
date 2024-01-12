import os
import pickle
import hashlib
import inspect
import re
import time

from colorama import Fore, Back, Style

def find_project_root(current_dir):
    """
    向上搜索直到找到标识文件，确定项目的根目录
    """
    # 检查当前目录是否包含标识文件
    if os.path.isfile(os.path.join(current_dir, '.projectroot')):
        return current_dir
    # 获取上一级目录
    parent_dir = os.path.dirname(current_dir)
    if parent_dir == current_dir:
        # 已经到达了文件系统的根目录
        raise FileNotFoundError("无法找到项目根目录标识文件, 请在项目根目录下创建 .projectroot 文件.")
    # 递归继续向上搜索
    return find_project_root(parent_dir)

def remove_unused_code(source_code):
    # 删除单行注释
    source_code = re.sub(r'#.*$', "", source_code, flags=re.MULTILINE)
    # 删除多行注释
    source_code = re.sub(r'""".*?"""', "", source_code, flags=re.MULTILINE | re.DOTALL)
    # 删除print语句
    source_code = re.sub(r'print\(.*\)', "", source_code)
    # 删除注解
    source_code = re.sub(r'@.*\(.*\)', '', source_code)
    return source_code

def cache(cache_dir, exclude=None, is_print=True):
    """
    缓存函数的装饰器
    :param cache_dir: 缓存目录
    :param exclude: 排除的参数 ['func_name', 'source_code', 'args'] 函数名、源代码、函数参数

    """
    if exclude is None:
        exclude = []

    def decorator(func):
        def wrapper(*args, **kwargs):
            # 获取函数的源代码，并删除所有空格和空行
            source_code = inspect.getsource(func)

            # 获取函数的参数名
            params = inspect.signature(func).parameters
            # 创建一个字典，将参数名和值对应起来
            args_dict = {name: kwargs.get(name, param.default) if param.default is not inspect.Parameter.empty else args[i] for i, (name, param) in enumerate(params.items())}
            args_dict.update(kwargs)
            # print('args_dict:', str(args_dict))
            # print('args:', args)
            # print('kwargs:', kwargs)

            # 使用参数值来修改路径
            modified_cache_dir = cache_dir.format(**args_dict)
            # print('modified_cache_dir:', modified_cache_dir)

            # 当前文件的绝对路径
            current_file_path = os.path.abspath(__file__)

            # 项目根目录的路径
            project_root = find_project_root(os.path.dirname(current_file_path))




            hash_key = []
            if 'func_name' not in exclude:
                hash_key.append(func.__name__)
            if 'source_code' not in exclude:
                tmp_source_code = source_code
                if 'func_name' not in exclude:
                    tmp_source_code = remove_unused_code(tmp_source_code)
                    tmp_source_code = tmp_source_code.replace(func.__name__, '')

                tmp_source_code = re.sub(r'\s', '', tmp_source_code)
                hash_key.append(tmp_source_code)
            if 'args' not in exclude:
                hash_key.append(str(args_dict))

            # 创建一个唯一的文件名，基于函数名、源代码和参数
            key = pickle.dumps(hash_key)
            file_name = hashlib.sha256(key).hexdigest() + '.pickle'
            file_path = os.path.join(project_root, modified_cache_dir, file_name)
            # print(file_path)
            # 创建缓存目录
            os.makedirs(os.path.join(project_root, modified_cache_dir), exist_ok=True)

            # 如果缓存文件存在，直接读取并返回结果
            if os.path.exists(file_path):
                start = time.time()
                if is_print:
                    print(Fore.GREEN + f'{func.__name__} Loading from cache {file_path}', Style.RESET_ALL, end=' ')
                with open(file_path, 'rb') as f:
                    try:
                        result = pickle.load(f)
                    except: # 如果pickle文件损坏，重新运行函数
                        result = func(*args, **kwargs)
                        with open(file_path, 'wb') as f:
                            pickle.dump(result, f)
                        if is_print:
                            print(Fore.YELLOW + f'{func.__name__} Saved to cache', file_path, Style.RESET_ALL)
                if is_print:
                    print(Fore.RED +f'{(time.time() - start):.1f}s ok', Style.RESET_ALL)
            else:
                # 否则，运行函数并保存结果
                result = func(*args, **kwargs)
                with open(file_path, 'wb') as f:
                    pickle.dump(result, f)
                if is_print:
                    print(Fore.YELLOW + f'{func.__name__} Saved to cache', file_path, Style.RESET_ALL)
            return result
        return wrapper
    return decorator
