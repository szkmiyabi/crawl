# -*- coding: utf-8 -*-
import scrapy
from scrapytest.items import Headline

class WelSpider(scrapy.Spider):
    name = 'wel'
    allowed_domains = ['www.wel.ne.jp']
    start_urls = ['https://www.wel.ne.jp/bbs/view/jiritsu/index.html']

    def parse(self, response):
        for url in response.css('.bbs_parent_header h2 a::attr("href")').re(r'/bbs/article/\d+\.html$'):
            yield scrapy.Request(response.urljoin(url), self.parse_topics)
    
    def parse_topics(self, response):
        item = Headline()
        item['title'] = response.css('.bbs_parent_header h1').xpath('string()').extract_first()
        item['body'] = response.css('.bbs_parent_body p').xpath('string()').extract_first()
        yield item
