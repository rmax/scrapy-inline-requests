import os
from setuptools import setup

LONG_DESC = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()


setup(
    name='scrapy-inline-requests',
    version='0.1.2',
    description='Scrapy decorator for inline requests',
    long_description=LONG_DESC,
    author='Rolando Espinoza La fuente',
    author_email='darkrho@gmail.com',
    url='https://github.com/darkrho/scrapy-inline-requests',
    license='BSD',
    py_modules=['inline_requests'],
    install_requires=[
        'Scrapy>=0.14',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
    ],
)
