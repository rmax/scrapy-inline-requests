from urlparse import urljoin

from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from scrapy.item import Item, Field
from scrapy.selector import HtmlXPathSelector

from inline_requests import inline_requests


class UserItem(Item):
    name = Field()
    website = Field()
    location = Field()
    answers = Field()
    questions = Field()
    tags = Field()
    url = Field()


class UserLoader(XPathItemLoader):
    default_item_class = UserItem
    default_output_processor = TakeFirst()


class StackoverflowSpider(CrawlSpider):
    name = "stackoverflow"
    allowed_domains = ["stackoverflow.com"]
    start_urls = (
        'http://stackoverflow.com/users',
    )

    rules = (
        Rule(SgmlLinkExtractor(allow=r'/users/\d+/'), callback='parse_profile'),
        # follow only first pages in pagination links
        Rule(SgmlLinkExtractor(allow=r'\?page=\d&')),
    )

    @inline_requests
    def parse_profile(self, response):
        base_url = response.url

        ul = UserLoader(response=response)
        ul.add_xpath('name', '//h1[1]/text()')
        ul.add_xpath('website', '//*[@rel="me" and @class="url"]/text()')
        ul.add_xpath('location', '//*[@class="label adr"]/text()')
        ul.add_value('url', base_url)
        item = ul.load_item()

        # scrape answers
        response = yield Request(base_url + '?tab=answers', priority=100)
        hxs = HtmlXPathSelector(response)

        answers = item['answers'] = []
        for link in hxs.select('//*[@class="answer-link"]/a'):
            href, title = self._get_href_text(link)
            answers.append({
                'title': title,
                'url': urljoin(response.url, href),
            })

        # scrape questions
        response = yield Request(base_url + '?tab=questions', priority=200)
        hxs = HtmlXPathSelector(response)

        questions = item['questions'] = []
        for link in hxs.select('//*[@class="user-questions"]//h3/a'):
            href, title = self._get_href_text(link)
            questions.append({
                'title': title,
                'url': urljoin(response.url, href)
            })

        # scrape tags
        response = yield Request(base_url + '?tab=tags', priority=300)
        hxs = HtmlXPathSelector(response)
        item['tags'] = hxs.select('//*[@class="user-tags"]//*[@class="post-tag"]/text()').extract()

        # finally yield our item
        yield item

    def _get_href_text(self, link):
        return (
            link.select('@href').extract()[0],
            link.select('text()').extract()[0]
        )

