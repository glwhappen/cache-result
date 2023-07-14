import os
import pickle
import hashlib
import inspect
import re
from colorama import Fore, Back, Style

def remove_comments_and_prints(source_code):
    # 删除单行注释
    source_code = re.sub(r'#.*$', "", source_code, flags=re.MULTILINE)
    # 删除print语句
    source_code = re.sub(r'print\(.*\)', "", source_code)
    return source_code

def cache(cache_dir, exclude=None, is_print=True):
    """
    缓存函数的装饰器
    :param cache_dir: 缓存目录
    :param exclude: 排除的参数 ['func_name', 'source_code', 'args', 'kwargs']

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

            # 使用参数值来修改路径
            modified_cache_dir = cache_dir.format(**args_dict)


            hash_key = []
            if 'func_name' not in exclude:
                hash_key.append(func.__name__)
            if 'source_code' not in exclude:
                tmp_source_code = source_code
                if 'func_name' not in exclude:
                    tmp_source_code = remove_comments_and_prints(tmp_source_code)
                    tmp_source_code = tmp_source_code.replace(func.__name__, '')

                tmp_source_code = re.sub(r'\s', '', tmp_source_code)
                hash_key.append(tmp_source_code)
            if 'args' not in exclude:
                hash_key.append(str(args))
            if 'kwargs' not in exclude:
                hash_key.append(str(kwargs))

            # 创建一个唯一的文件名，基于函数名、源代码和参数
            key = pickle.dumps(hash_key)
            file_name = hashlib.sha256(key).hexdigest() + '.pickle'
            file_path = os.path.join(modified_cache_dir, file_name)

            # 创建缓存目录
            os.makedirs(modified_cache_dir, exist_ok=True)

            # 如果缓存文件存在，直接读取并返回结果
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    try:
                        result = pickle.load(f)
                    except: # 如果pickle文件损坏，重新运行函数
                        result = func(*args, **kwargs)
                        with open(file_path, 'wb') as f:
                            pickle.dump(result, f)
                        if is_print:
                            print(Fore.YELLOW + f'{func.__name__} Saved to cache', os.path.join(os.getcwd(), modified_cache_dir))
                            print(Style.RESET_ALL)
                if is_print:
                    print(Fore.GREEN +f'{func.__name__} Loaded from cache')
                    print(Style.RESET_ALL)
            else:
                # 否则，运行函数并保存结果
                result = func(*args, **kwargs)
                with open(file_path, 'wb') as f:
                    pickle.dump(result, f)
                if is_print:
                    print(Fore.YELLOW + f'{func.__name__} Saved to cache', os.path.join(os.getcwd(), modified_cache_dir))
                    print(Style.RESET_ALL)
            return result
        return wrapper
    return decorator
