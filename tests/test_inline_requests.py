#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_inline_requests
----------------------------------

Tests for `inline_requests` module.
"""
from scrapy.http import Request, Response

from inline_requests import inline_requests


def _consume(callback, *args):
    req = next(callback(*args))
    while req:
        yield req
        try:
            req = next(req.callback(Response(req.url)))
        except (TypeError, StopIteration):
            break


def test_inline_requests():

    class MySpider(object):
        @inline_requests
        def parse(self, response):
            yield Request('http://example/1')
            yield Request('http://example/2')

    spider = MySpider()
    out = [req.url for req in _consume(spider.parse, Response('http://example'))]
    assert out == [
        'http://example/1',
        'http://example/2',
    ]
