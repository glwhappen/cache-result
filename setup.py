from setuptools import setup, find_packages

# 读取README.md文件的内容
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cache-result',
    version='0.1.2',
    description='A decorator for caching the results of functions',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='glwhappen',
    author_email='1597721684@qq.com',
    packages=find_packages(),
    install_requires=[],
)