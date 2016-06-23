import os
from setuptools import setup

LONG_DESC = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()


setup(
    name='scrapy-inline-requests',
    version='0.2.0',
    description='Scrapy decorator for inline requests',
    long_description=LONG_DESC,
    author='Rolando Espinoza La fuente',
    author_email='darkrho@gmail.com',
    url='https://github.com/rolando/scrapy-inline-requests',
    license='BSD',
    py_modules=['inline_requests'],
    install_requires=[
        'six>=1.5.2',
        'Scrapy>=1.0',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
    ],
)
