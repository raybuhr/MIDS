# -*- coding: utf-8 -*-
import scrapy


class HuffySpider(scrapy.Spider):
    name = "huffy"
    allowed_domains = ["www.huffingtonpost.com"]
    start_urls = (
        'http://www.huffingtonpost.com/',
    )

    def parse(self, response):
        pass
