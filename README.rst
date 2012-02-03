Scrapy Inline Requests
======================

This module provides a decorator to allow to write spider callbacks
which performs multiple requests without the need to write multiple
callbacks for each request.

Example::

  def parse_item(self, response):
    item = self.build_item(response)

    # scrape more information
    response = yield Request(response.url + '?info')
    item['info'] = self.extract_info(response)

    # scrape pictures
    response = yield Request(response.url + '?pictures')
    item['pictures'] = self.extract_pictures(response)

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
