Scrapy Inline Requests
======================

This module provides a decorator to allow to write Scrapy_'s spider
callbacks which performs multiple requests without the need to write
multiple callbacks for each request.

The code still *experimental* and might not work in all cases.

Example::

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

* Python 2.6+
* Scrapy 0.14+

.. _Scrapy: http://www.scrapy.org
