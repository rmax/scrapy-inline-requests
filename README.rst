Scrapy Inline Requests
======================

This module provides a decorator that allows to write coroutine-like spider callbacks.

The code is **experimental**, might not work in all cases and even might be
hard to debug.

Example:

.. code:: python

  from inline_requests import inline_requests

  class MySpider(CrawlSpider):

    ...

    @inline_requests
    def parse_item(self, response):
      item = self.build_item(response)

      # scrape more information
      response = yield Request(response.url + '?info')
      item['info'] = self.extract_info(response)

      # scrape pictures
      response = yield Request(response.url + '?pictures')
      item['pictures'] = self.extract_pictures(response)

      # a request that might fail (dns error, network timeout, error 404/500, etc)
      try:
        response = yield Request(response.url + '?protected')
      except Exception as e:
        log.err(e, spider=self)
      else:
        item['protected'] = self.extract_protected_info(response)

      # finally yield the item
      yield item


Example Project
---------------

The `example` directory includes a example spider for StackOverflow.com::

  cd example
  scrapy crawl stackoverflow

Requirements
------------

* Python 2.7+, 3.4+
* Scrapy 1.0+

Known Issues
------------

* Middlewares can drop or ignore non-200 status responses causing the callback to not continue its execution. This can be overcome by using the flag ``handle_httpstatus_all``. See the `httperror`_ middleware documentation.
* High concurrency and large responses can cause higher memory usage.


.. _Scrapy: http://www.scrapy.org
.. _httperror: http://doc.scrapy.org/en/latest/topics/spider-middleware.html#module-scrapy.spidermiddlewares.httperror
