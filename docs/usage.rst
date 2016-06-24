=====
Usage
=====

To use Scrapy Inline Requests in a project::

    from inline_requests import inline_requests

Limitations
-----------

* The decorated spider method must have the signature ``(self, response)``.
* The yielded request should not have a callback set, otherwise it could lead
  to not getting back the response.
* Ensure you don't miss any unhandled response (i.e.: due to response status).
