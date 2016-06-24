===============================
Scrapy Inline Requests
===============================

.. image:: https://img.shields.io/pypi/v/scrapy-inline-requests.svg
        :target: https://pypi.python.org/pypi/scrapy-inline-requests

.. image:: https://img.shields.io/travis/rolando/scrapy-inline-requests.svg
        :target: https://travis-ci.org/rolando/scrapy-inline-requests

.. image:: https://readthedocs.org/projects/scrapy-inline-requests/badge/?version=latest
        :target: https://readthedocs.org/projects/scrapy-inline-requests/?badge=latest
        :alt: Documentation Status


A decorator for writing coroutine-like spider callbacks.

Requires ``Scrapy>=1.0`` and supports Python 2.7+ and 3.4+.

* Free software: MIT license
* Documentation: https://scrapy-inline-requests.readthedocs.org.

Usage
=====

The spider below shows a simple use case of scraping a page and following a few links:

.. code:: python

    from scrapy import Spider, Request
    from inline_requests import inline_requests

    class MySpider(Spider):
        name = 'myspider'
        start_urls = ['http://httpbin.org/html']

        @inline_requests
        def parse(self, response):
            urls = [response.url]
            for i in range(10):
                next_resp = yield Request(response.urljoin('?page=%d' % i))
                urls.append(next_resp.url)
            yield {'urls': urls}


See the ``examples/`` directory for a more complex spider.


Known Issues
============

* Middlewares can drop or ignore non-200 status responses causing the callback
  to not continue its execution. This can be overcome by using the flag
  ``handle_httpstatus_all``. See the `httperror middleware`_ documentation.
* High concurrency and large responses can cause higher memory usage.
* This decorator assumes your method have the following signature
  ``(self, response)``.
* The decorated method must return a **generator** instance.

.. _`httperror middleware`: http://doc.scrapy.org/en/latest/topics/spider-middleware.html#scrapy.spidermiddlewares.httperror.HttpErrorMiddleware
