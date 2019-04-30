# -*- coding: utf-8 -*-
import scrapy


class BellezaSpider(scrapy.Spider):
    name = 'belleza'
    allowed_domains = ['simple.ripley.com.pe']
    start_urls = ['http://simple.ripley.com.pe/']

    def parse(self, response):
        pass
