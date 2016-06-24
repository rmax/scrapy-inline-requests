#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pkgutil import walk_packages
from setuptools import setup


def find_packages(path):
    # This method returns packages and subpackages as well.
    for _, name, is_pkg in walk_packages([path]):
        if is_pkg:
            yield name


def read_file(filename):
    with open(filename) as fp:
        return fp.read()


requirements = [
    'six>=1.5',
    'scrapy>=1.0',
]

setup(
    name='scrapy-inline-requests',
    version='0.3.0',
    description="A decorator for writing coroutine-like spider callbacks.",
    long_description=read_file('README.rst') + '\n\n' + read_file('HISTORY.rst'),
    author="Rolando Espinoza",
    author_email='rolando at rmax.io',
    url='https://github.com/rolando/scrapy-inline-requests',
    packages=list(find_packages('src')),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=True,
    keywords='scrapy-inline-requests',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
