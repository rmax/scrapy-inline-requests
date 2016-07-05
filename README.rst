======================
Scrapy Inline Requests
======================

.. image:: https://img.shields.io/pypi/v/scrapy-inline-requests.svg
        :target: https://pypi.python.org/pypi/scrapy-inline-requests

.. image:: https://img.shields.io/pypi/pyversions/scrapy-inline-requests.svg
        :target: https://pypi.python.org/pypi/scrapy-inline-requests

.. image:: https://readthedocs.org/projects/scrapy-inline-requests/badge/?version=latest
        :target: https://readthedocs.org/projects/scrapy-inline-requests/?badge=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/travis/rolando/scrapy-inline-requests.svg
        :target: https://travis-ci.org/rolando/scrapy-inline-requests

.. image:: https://codecov.io/github/rolando/scrapy-inline-requests/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/rolando/scrapy-inline-requests

.. image:: https://landscape.io/github/rolando/scrapy-inline-requests/master/landscape.svg?style=flat
    :target: https://landscape.io/github/rolando/scrapy-inline-requests/master
    :alt: Code Quality Status

.. image:: https://requires.io/github/rolando/scrapy-inline-requests/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/rolando/scrapy-inline-requests/requirements/?branch=master

A decorator for writing coroutine-like spider callbacks.

* Free software: MIT license
* Documentation: https://scrapy-inline-requests.readthedocs.org.
* Python versions: 2.7, 3.4+

Quickstart
----------

The spider below shows a simple use case of scraping a page and following a few links:

.. code:: python

    from inline_requests import inline_requests
    from scrapy import Spider, Request

    class MySpider(Spider):
        name = 'myspider'
        start_urls = ['http://httpbin.org/html']

        @inline_requests
        def parse(self, response):
            urls = [response.url]
            for i in range(10):
                next_url = response.urljoin('?page=%d' % i)
                try:
                    next_resp = yield Request(next_url)
                    urls.append(next_resp.url)
                except Exception:
                    self.logger.info("Failed request %s", i, exc_info=True)

            yield {'urls': urls}


See the ``examples/`` directory for a more complex spider.

.. warning::

  The generator resumes its execution when a request's response is processed,
  this means the generator won't be resume after yielding an item or a request
  with it's own callback.


Known Issues
------------

* Middlewares can drop or ignore non-200 status responses causing the callback
  to not continue its execution. This can be overcome by using the flag
  ``handle_httpstatus_all``. See the `httperror middleware`_ documentation.
* High concurrency and large responses can cause higher memory usage.
* This decorator assumes your method have the following signature
  ``(self, response)``.
* Wrapped requests may not be able to be serialized by persistent backends.
* Unless you know what you are doing, the decorated method must be a spider
  method and return a **generator** instance.

.. _`httperror middleware`: http://doc.scrapy.org/en/latest/topics/spider-middleware.html#scrapy.spidermiddlewares.httperror.HttpErrorMiddleware
