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
            resp = Response(req.url, request=req)
            req = next(req.callback(resp))
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


def test_inline_request_callback_not_allowed():
    class MySpider(object):
        @inline_requests
        def parse(self, response):
            resp = yield Request('http://example/1')
            assert resp.request.callback is None
            assert resp.request.errback is None

    spider = MySpider()
    _consume(spider.parse(Response('http://example.com')))
