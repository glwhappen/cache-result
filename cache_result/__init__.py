import os
import pickle
import hashlib
import inspect
import re


def cache(cache_dir, exclude=None, is_print=False):
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
            args_dict = {list(params.keys())[i]: arg for i, arg in enumerate(args)}
            args_dict.update(kwargs)

            # 使用参数值来修改路径
            modified_cache_dir = cache_dir.format(**args_dict)


            hash_key = []
            if 'func_name' not in exclude:
                hash_key.append(func.__name__)
            if 'source_code' not in exclude:
                tmp_source_code = source_code
                if 'func_name' not in exclude:
                    tmp_source_code = source_code.replace(func.__name__, '')

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
                    result = pickle.load(f)
                if is_print:
                    print('Loaded from cache')
            else:
                # 否则，运行函数并保存结果
                result = func(*args, **kwargs)
                with open(file_path, 'wb') as f:
                    pickle.dump(result, f)
                if is_print:
                    print('Saved to cache')
            return result
        return wrapper
    return decorator
