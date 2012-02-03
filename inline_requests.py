import types
from functools import partial

from scrapy.http import Request
from scrapy.utils.spider import iterate_spider_output


def inline_requests(method):
    """Decorator to enable inline requests"""
    def wrapper(self, response):
        callback = types.MethodType(method, self, self.__class__)
        genwrapper = _RequestGenerator(callback)
        return genwrapper(response)
    return wrapper


class _RequestGenerator(object):

    def __init__(self, callback):
        self.callback = callback

    def __call__(self, response):
        output = iterate_spider_output(self.callback(response))
        if isinstance(output, types.GeneratorType):
            return self._unwindGenerator(output)
        else:
            return output

    def _unwindGenerator(self, generator, _prev=None):
        while True:
            if _prev:
                ret, _prev = _prev, None
            else:
                try:
                    ret = generator.next()
                except StopIteration:
                    break
            if isinstance(ret, Request) and ret.callback is None:
                yield self._wrapRequest(ret, generator)
                break
            else:
                yield ret

    def _wrapRequest(self, request, generator):
        request.callback = partial(self._handleSuccess, generator=generator)
        request.errback = partial(self._handleFailure, generator=generator)
        return request

    def _handleSuccess(self, response, generator):
        try:
            ret = generator.send(response)
        except StopIteration:
            return
        return self._unwindGenerator(generator, ret)

    def _handleFailure(self, failure, generator):
        try:
            ret = failure.throwExceptionIntoGenerator(generator)
        except StopIteration:
            return
        return self._unwindGenerator(generator, ret)

