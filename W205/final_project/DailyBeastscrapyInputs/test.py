from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from beastCrl.items import BeastcrlItem
from scrapy import Request
import datetime

class MySpider(Spider):
    name = "beastCrl"
    allowed_domains = ["thedailybeast.com"]
    
    start_urls = []
    for page in range(2500):
      url = "http://www.thedailybeast.com/search.html?type=stories&order=date&page="+str(page)+"&_charset_=utf-8"
      start_urls.append(url)
    
    def parse(self, response):
      hxs = HtmlXPathSelector(response)
      articlelinks = hxs.select("//h2[@class='heading heading-style-p']")
      bodyText = hxs.select("//section[@class='content-body article-body-content']")
      bodyText = hxs.select("//section[@class='content-body article-body-content']")
      title = hxs.select("//h1[@class='title multiline']")
      datetime = hxs.select("//div[@class='publish-date-time']")
      
      #print len(bodyText)
      
      if len(bodyText)>0:
        item = BeastcrlItem()
        item["datetime"] = datetime[0].extract()
        item["title"] = title[0].extract()
        item["body"] = bodyText[0].extract()
        #item["body"] = "BODY TEXT HERE"
        yield item
    
      '''
      print "len(articlelinks = "+str(len(articlelinks))
      for articlelink in articlelinks:
        print "articlelink: "+str(articlelinks.select("a/@href").extract())
        item = BeastcrlItem()
        item ["link"] = articlelink.select("a/@href").extract()
      return item
      '''

      #for title in titles:
      urls = articlelinks.select("a/@href").extract()
      for url in urls:
        yield Request("http://www.thedailybeast.com"+url, callback=self.parse)


