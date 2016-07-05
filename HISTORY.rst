=======
History
=======

.. comment:: bumpversion marker

0.3.1 (2016-07-04)
------------------

* Added deprecation about decorating non-spider functions.
* Warn if the callback returns requests with callback or errback set. This
  reverts the compability with requests with callbacks.

0.3.0 (2016-06-24)
------------------
* ~~Backward incompatible change: Added more restrictions to the request object (no callback/errback).~~
* Cleanup callback/errback attributes before sending back the request to the
  generator. This fixes an edge case when using ``request.replace()``.
* Simplified example spider.

0.2.0 (2016-06-23)
------------------

* Python 3 support.


0.1.2 (2016-05-22)
------------------

* Scrapy API and documentation updates.

0.1.1 (2013-02-03)
------------------

* Minor tweaks and fixes.

0.1.0 (2012-02-03)
------------------

* First release on PyPI.
