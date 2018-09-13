#!/usr/bin/env python3

from setuptools import setup, find_packages
import re
import io

with open('README.md', 'r') as f:
    long_description = f.read()

with io.open('codechef_cli/__version__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)


setup(
    name='codechef-cli',
    version=version,
    author='Vishnunarayan K.I., Mrigank Krishan',
    author_email='vishnunarayan6105@gmail.com, mrigankkrishan@gmail.com',
    description='Use codechef from the comforts of your terminal.',
    packages=find_packages(),
    url='https://github.com/vn-ki/codechef-cli',
    keywords=['codechef', 'cli'],
    install_requires=[
        'requests>=2.18.4',
        'Click>=6.7',
        'flask>=1.0.2',
        'tabulate>=0.8.2',
        'inscriptis>=0.0.3.2',
        'picotui>=1.0',
        'lxml',
        'coloredlogs==10.0'
    ],
    tests_require=[
        'pytest',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points='''
        [console_scripts]
        codechef=codechef_cli.cli:cli
    '''
)
