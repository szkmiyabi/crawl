# -*- coding: utf-8 -*-
import scrapy
from scrapytest.items import Headline

class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['news.yahoo.co.jp']
    start_urls = ['https://news.yahoo.co.jp/']

    def parse(self, response):
        #print(response.css('ul.topics a::attr("href")').extract())
        for url in response.css('ul.toptopics_list a::attr("href")').re(r'/pickup/\d+$'):
            yield scrapy.Request(response.urljoin(url), self.parse_topics)
    
    def parse_topics(self, response):
        item = Headline()
        item['title'] = response.css('.newsTitle a::text').extract_first()
        item['body'] = response.css('.hbody').xpath('string()').extract_first()
        yield item
