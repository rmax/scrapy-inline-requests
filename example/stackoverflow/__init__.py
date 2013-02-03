# Scrapy settings for example project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

import os.path
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.realpath(__file__)
))))


SPIDER_MODULES = ['stackoverflow']
NEWSPIDER_MODULE = 'stackoverflow'

CONCURRENT_REQUESTS = 1
CONCURRENT_ITEMS = 1
