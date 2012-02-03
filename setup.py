from setuptools import setup

setup(name='scrapy-inline-requests',
      version='0.1',
      description='Scrapy decorator for inline requests',
      author='Rolando Espinoza La fuente',
      author_email='darkrho@gmail.com',
      url='https://github.com/darkrho/scrapy-inline-requests',
      license='BSD',
      py_modules = ['inline_requests'],
      install_requires=[
          'Scrapy>=0.14',
      ],
      classifiers=[
          'Programming Language :: Python',
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
      ],
     )
