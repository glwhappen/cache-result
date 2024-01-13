import datetime
import os
import pickle
import hashlib
import inspect
import re
import sys
import time
from loguru import logger

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

def _remove_unused_code(source_code):
    # 删除单行注释
    source_code = re.sub(r'#.*$', "", source_code, flags=re.MULTILINE)
    # 删除多行注释
    source_code = re.sub(r'""".*?"""', "", source_code, flags=re.MULTILINE | re.DOTALL)
    # 删除print语句
    source_code = re.sub(r'print\(.*\)', "", source_code)
    # 删除注解
    source_code = re.sub(r'@.*\(.*\)', '', source_code)
    # 删除def所在的行
    source_code = re.sub(r'\bdef\s+[\w_]+\s*\([^)]*\):', '', source_code)
    return source_code


def _to_cache(func, file_path, result, is_print):
    with open(file_path, 'wb') as f:
        pickle.dump(result, f)
    if is_print:
        print(Fore.YELLOW + f'{func.__name__} Saved to cache', file_path, Style.RESET_ALL)


def format_cache_time(cache_dir_format):
    """
    格式化缓存目录字符串中的时间占位符。
    :param cache_dir_format: 带有时间占位符的缓存目录格式。
    :return: 格式化后的缓存目录字符串。
    """

    # 定义一个函数，用于将用户定义的时间格式转换为 datetime 可以识别的格式
    def format_time_string(time_format):
        format_mappings = {
            "YYYY": "%Y",
            "MM": "%m",   # 月份
            "DD": "%d",
            "HH": "%H",   # 小时
            "mm": "%M",   # 分钟
            "ss": "%S"    # 秒
        }
        for key, value in format_mappings.items():
            time_format = time_format.replace(key, value)
        return time_format

    # 使用正则表达式查找时间格式占位符
    time_format_match = re.search(r'\{time:(.+?)\}', cache_dir_format)
    if time_format_match:
        user_defined_format = time_format_match.group(1)
        datetime_format = format_time_string(user_defined_format)
        current_time = datetime.datetime.now().strftime(datetime_format)
        formatted_cache_dir = re.sub(r'\{time:.+?\}', current_time, cache_dir_format)
    else:
        formatted_cache_dir = cache_dir_format

    return formatted_cache_dir

def cache(cache_dir='cache', is_print=True, is_print_path = False, has_source_code=True, exclude_args: list[str]=None, debug=False, hash_length=16):
    """
    缓存函数的装饰器
    :param cache_dir: 缓存目录，支持时间格式化
    :param is_print: 是否打印缓存使用信息
    :param is_print_path: 是否打印缓存路径
    :param has_source_code: 是否包含源代码
    :param exclude_args: 排除的参数列表
    :param debug: 是否开启debug模式
    :param hash_length: 缓存文件名的哈希长度
    """
    if exclude_args is None:
        exclude_args = []
    logger.remove()
    if debug:
        logger.add(sys.stderr, level="DEBUG", enqueue=False)
    else:
        logger.add(sys.stderr, level="WARNING", enqueue=False)

    def decorator(func):
        def wrapper(*args, **kwargs):
            # 获取函数的源代码，并删除所有空格和空行
            source_code = inspect.getsource(func)

            # 获取函数的参数名
            params = inspect.signature(func).parameters
            # 创建一个字典，将参数名和值对应起来
            args_dict = {name: kwargs.get(name) if name in kwargs else args[i] if i < len(args) else param.default for i, (name, param) in enumerate(params.items())}

            logger.debug(f"row args_dict: {args_dict}")
            args_dict.update(kwargs)
            logger.debug(f"row args_dict update(kwargs): {args_dict}")
            args_dict = {key: value for key, value in args_dict.items() if key not in exclude_args}

            logger.debug(f"filtered args_dict: {args_dict}")
            sorted(args_dict)
            logger.debug(f"sorted args_dict: {args_dict}")
            # print('args_dict:', str(args_dict))
            # print('args:', args)
            # print('kwargs:', kwargs)
            logger.debug(f"row cache_dir: {cache_dir}")
            modified_cache_dir = cache_dir
            # 格式化 cache_dir 中的时间占位符
            modified_cache_dir = format_cache_time(modified_cache_dir)
            logger.debug(f"row cache_dir add time: {modified_cache_dir}")
            # print('modified_cache_dir:', modified_cache_dir)

            # 使用参数值来修改路径
            modified_cache_dir = modified_cache_dir.format(**args_dict)
            logger.debug(f"row cache_dir add args: {modified_cache_dir}")

            # 当前文件的绝对路径
            current_file_path = os.path.abspath(__file__)

            # 项目根目录的路径
            project_root = find_project_root(os.path.dirname(current_file_path))

            # 创建缓存目录
            os.makedirs(os.path.join(project_root, modified_cache_dir), exist_ok=True)


            hash_key = []
            hash_key.append(str(args_dict))

            if has_source_code:
                tmp_source_code = source_code
                tmp_source_code = _remove_unused_code(tmp_source_code)
                tmp_source_code = re.sub(r'\s', '', tmp_source_code)
                logger.debug(f"add source_code: {tmp_source_code}")
                hash_key.append(tmp_source_code)

            logger.info(f"hash_key content: {hash_key}")
            # 创建一个唯一的文件名，基于函数名、源代码和参数
            key = pickle.dumps(hash_key)
            logger.debug(f"hash_key to key: {hashlib.sha256(key).hexdigest()}")
            logger.info(f"key to short: {hashlib.sha256(key).hexdigest()[:hash_length]}")
            file_name = hashlib.sha256(key).hexdigest()[:hash_length] + '.pickle'
            file_path = os.path.join(project_root, modified_cache_dir, file_name)

            if is_print_path:
                show_file_name = file_path
            else:
                show_file_name = os.path.join(modified_cache_dir, file_name)
            # 如果缓存文件存在，直接读取并返回结果
            if os.path.exists(file_path):
                start = time.time()
                if is_print:
                    print(Fore.GREEN + f'{func.__name__} Loading from cache {show_file_name}', Style.RESET_ALL, end=' ')
                with open(file_path, 'rb') as f:
                    try:
                        result = pickle.load(f)
                    except:  # 如果pickle文件损坏，重新运行函数
                        result = func(*args, **kwargs)
                        _to_cache(func, file_path, result, is_print)
                if is_print:
                    print(Fore.RED + f'{(time.time() - start):.1f}s ok', Style.RESET_ALL)
            else:
                # 否则，运行函数并保存结果
                result = func(*args, **kwargs)
                _to_cache(func, file_path, result, is_print)
                if has_source_code:
                    # 包含代码了，多创建一个不包含代码的
                    logger.debug("哈希值包含了代码，多创建一个不包含代码的，方便后续更多操作")
                    key = pickle.dumps([str(args_dict)])

                    file_name = hashlib.sha256(key).hexdigest()[:hash_length] + '.pickle'
                    file_path = os.path.join(project_root, modified_cache_dir, file_name)
                    _to_cache(func, file_path, result, is_print)


            return result
        return wrapper
    return decorator
