#!/usr/bin/env python3
from setuptools import setup

with open('README.md') as readme:
    long_description = readme.read()


setup(
    name='pyraddb',
    version='0.0.1',
    description='Play with FreeRADIUS database, easy to manage users and groups.',
    author='XiErCh',
    author_email='orz@sorz.org',
    url='https://github.com/sorz/pyraddb/',
    packages=['pyraddb'],
    data_files=[('', ['README.md'])],
    install_requires=['mysql-connector-python'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
    ],
    long_description=long_description
)
