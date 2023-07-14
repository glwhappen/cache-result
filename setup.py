from setuptools import setup, find_packages

# 读取README.md文件的内容
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cache-result',
    version='0.1.5',
    description='A python decorator for caching the results of functions',
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        'Source Code': 'https://github.com/glwhappen/cache-result',
    },
    author='glwhappen',
    author_email='1597721684@qq.com',
    packages=find_packages(),
    install_requires=[],
)