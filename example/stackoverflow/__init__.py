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


BOT_NAME = 'SOBot'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['stackoverflow']
NEWSPIDER_MODULE = 'stackoverflow'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

CONCURRENT_REQUESTS = 1
CONCURRENT_ITEMS = 1
