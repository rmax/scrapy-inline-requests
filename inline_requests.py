import inspect
import types
from functools import partial, wraps

from scrapy.http import Request
from scrapy.utils.spider import iterate_spider_output


def inline_requests(method_or_func):
    args = inspect.getargspec(method_or_func).args
    if not args:
        raise TypeError("Function must accept at least one argument.")
    # XXX: hardcoded convention of 'self' as first argument for methods
    if args[0] == 'self':
        def wrapper(self, response, **kwargs):
            callback = types.MethodType(method_or_func, self, self.__class__)
            genwrapper = _RequestGenerator(callback, **kwargs)
            return genwrapper(response)
    else:
        def wrapper(response, **kwargs):
            genwrapper = _RequestGenerator(method_or_func, **kwargs)
            return genwrapper(response)

    return wraps(method_or_func)(wrapper)


class _RequestGenerator(object):

    def __init__(self, callback, **kwargs):
        self.callback = callback
        self.kwargs = kwargs

    def __call__(self, response):
        output = iterate_spider_output(self.callback(response=response, **self.kwargs))
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
            if isinstance(ret, Request):
                yield self._wrapRequest(ret, generator)
                break
            else:
                yield ret

    def _wrapRequest(self, request, generator):
        request.callback = partial(self._handleSuccess, callback=request.callback, generator=generator)
        request.errback = partial(self._handleFailure, errback=request.errback, generator=generator)
        return request

    def _handleSuccess(self, response, callback, generator):
        try:
            if callback:
                ret = generator.send(callback(response))
            else:
                ret = generator.send(response)
        except StopIteration:
            return
        return self._unwindGenerator(generator, ret)

    def _handleFailure(self, failure, errback, generator):
        try:
            if errback:
                try:
                    ret = errback(failure)
                except:
                    ret = failure.throwExceptionIntoGenerator(generator)
                else:
                    ret = generator.send(ret)
            else:
                ret = failure.throwExceptionIntoGenerator(generator)
        except StopIteration:
            return
        return self._unwindGenerator(generator, ret)