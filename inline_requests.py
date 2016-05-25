import inspect
import types
from functools import partial, wraps
from six import create_bound_method

from scrapy.http import Request
from scrapy.utils.spider import iterate_spider_output


def _get_args(method_or_func):
    """
    Return method or function arguments.
    """
    try:
        # Python 3.0+
        args = list(inspect.signature(method_or_func).parameters.keys())
    except AttributeError:
        # Python 2.7
        args = inspect.getargspec(method_or_func).args
    return args

def inline_requests(method_or_func):
    args = _get_args(method_or_func)
    if not args:
        raise TypeError("Function must accept at least one argument.")
    # XXX: hardcoded convention of 'self' as first argument for methods
    if args[0] == 'self':
        def wrapper(self, response, **kwargs):
            callback = create_bound_method(method_or_func, self)
            
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
                    ret = next(generator)
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
