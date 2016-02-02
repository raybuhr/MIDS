# -*- coding: utf-8 -*-

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

class MySpider(BaseSpider):
	name = 'huff'
	allowed_domains = ['huffingtonpost.com']
	start_urls = ['http://www.huffingtonpost.com/search.php/?q=Search+The+Huffington+Post&type=blogs&s_it=header_form_v1']

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		titles = hxs.select("//p")
		for titles in titles:
			title = titles.select("a/text()").extract()
			link = titles.select("a/@href").extract()
			print title, link
