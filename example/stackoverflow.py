from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from inline_requests import inline_requests


class StackoverflowSpider(CrawlSpider):
    name = "stackoverflow"
    allowed_domains = ["stackoverflow.com"]
    start_urls = ['http://stackoverflow.com/users']
    user_agent = 'scrapy-inline-requests (+https://github.com/rolando/scrapy-inline-requests)'

    rules = [
        Rule(LinkExtractor(allow=r'/users/\d+/'), callback='parse_profile'),
        # Follow only first pages in pagination links.
        Rule(LinkExtractor(allow=r'\?page=\d&')),
    ]

    @inline_requests
    def parse_profile(self, response):
        # Scrape user info from user page.
        user = self.load_user(response)

        # Scrapy user's answers.
        answers_url = response.urljoin('?tab=answers')
        answers_resp = yield Request(answers_url)
        user['answers'] = list(
            self.iter_links(answers_resp, answers_resp.css('.answer-link'))
        )

        # Scrape user's questions.
        questions_url = response.urljoin('?tab=questions')
        questions_resp = yield Request(questions_url)
        user['questions'] = list(
            self.iter_links(questions_resp, questions_resp.css('.user-questions h3'))
        )

        # Scrape user's tags.
        tags_url = response.urljoin('?tab=tags')
        tags_resp = yield Request(tags_url)
        user['tags'] = tags_resp.css('.user-tags .post-tag::text').extract()

        # Item complete.
        yield user

    def load_user(self, response):
        return {
            'name': response.css('h1::text').extract_first(),
            'website': response.css('.url[rel=me]::text').extract_first(),
            'location': response.css('.label.adr::text').extract_first(),
            'url': response.url,
        }

    def iter_links(self, response, sel, expr='a[href]'):
        for link in sel.css(expr):
            yield {
                'title': link.css('::text').extract_first(),
                'url': response.urljoin(link.xpath('@href').extract_first()),
            }
