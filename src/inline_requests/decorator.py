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
    """A decorator to use coroutine-like spider callbacks.

    Example:

    .. code:: python

        class MySpider(Spider):

            @inline_callbacks
            def parse(self, response):
                next_url = response.urjoin('?next')
                try:
                    next_resp = yield Request(next_url)
                except Exception as e:
                    self.logger.exception("An error occurred.")
                    return
                else:
                    yield {"next_url": next_resp.url}


    You must conform with the following conventions:

    * The decorated method must be a spider method.
    * The decorated method must use the ``yield`` keyword or return a
    generator.
    * The decorated method must accept ``response`` as the first argument.
    * The decorated method must yield ``Request`` objects without neither
    ``callback`` nor ``errback`` set.

    If your requests don't come back to the generator try setting the flag to
    handle all http statuses:

    .. code:: python

                request.meta['handle_httpstatus_all'] = True

    """
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
        if not isinstance(output, types.GeneratorType):
            raise ValueError("Callback must return a generator type")
        return self._unwindGenerator(output)

    def _unwindGenerator(self, generator, _prev=None):
        while True:
            if _prev:
                ret, _prev = _prev, None
            else:
                try:
                    ret = next(generator)
                except StopIteration:
                    break
            if isinstance(ret, Request):
                yield self._wrapRequest(ret, generator)
                break
            else:
                yield ret

    def _wrapRequest(self, request, generator):
        # Allowing existing callback or errbacks could lead to undesired
        # results. To ensure the generator is **always** properly exhausted we
        # must handle both callback and errback in order to send back the
        # result to the generator.
        if request.callback is not None:
            raise ValueError("Request with existing callback is not supported")
        if request.errback is not None:
            raise ValueError("Request with existing callback is not supported")
        request.callback = partial(self._handleSuccess, generator=generator)
        request.errback = partial(self._handleFailure, generator=generator)
        return request

    def _cleanRequest(self, request):
        request.callback = None
        request.errback = None

    def _handleSuccess(self, response, generator):
        if response.request:
            self._cleanRequest(response.request)
        try:
            ret = generator.send(response)
        except StopIteration:
            return
        return self._unwindGenerator(generator, ret)

    def _handleFailure(self, failure, generator):
        # Look for the request instance in the exception value.
        if hasattr(failure.value, 'request'):
            self._cleanRequest(failure.value.request)
        elif hasattr(failure.value, 'response'):
            if hasattr(failure.value.response, 'request'):
                self._cleanRequest(failure.value.response.request)
        try:
            ret = failure.throwExceptionIntoGenerator(generator)
        except StopIteration:
            return
        return self._unwindGenerator(generator, ret)
