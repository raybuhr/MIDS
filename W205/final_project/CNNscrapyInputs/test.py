from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from cnnCrl.items import CnncrlItem
from scrapy import Request
import datetime

class MySpider(Spider):
    name = "cnnCrl"
    allowed_domains = ["transcripts.cnn.com"]
    
    currentdate = datetime.date(2015,4,13)
    start_urls = []
    for daycount in range(365):
      currentdate = currentdate-datetime.timedelta(days=1)
      currentyear = str(currentdate.year)
      currentmonth = str(currentdate.month)
      if currentdate.month<10:
        currentmonth = "0"+str(currentmonth)
      currentday = str(currentdate.day)
      if currentdate.day<10:
        currentday = "0"+str(currentday)
      url = "http://transcripts.cnn.com/TRANSCRIPTS/"+currentyear+"."+currentmonth+"."+currentday+".html"
      start_urls.append(url)

    #start_urls = ["http://transcripts.cnn.com/TRANSCRIPTS/2015.04.03.html"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.select("//div[@class='cnnSectBulletItems']")
	bodyText = hxs.select("//p[@class='cnnBodyText']")
	show = hxs.select("//p[@class='cnnTransStoryHead']")      	
	subhead = hxs.select("//p[@class='cnnTransSubHead']")      	

	if len(bodyText)>=3:
    		item = CnncrlItem()
		item["date"] = bodyText[-3].extract()
		item["show"] = show[0].extract()
		item["subhead"] = subhead.extract()
		item["body"] = bodyText[-1].extract()
		#item["body"] = "TEXT HERE"
		yield item
	#for text in bodyText:
        #        item = CnncrlItem()
        #        item ["link"] = text.extract()
	#		print text.extract()
        #        yield item

	#for titles in titles:
        #  	item = CnncrlItem()
        #  	item ["link"] = titles.select("a/@href").extract()
	#	yield item

	for title in titles:
		urls = titles.select("a/@href").extract()
		for url in urls:
			yield Request("http://transcripts.cnn.com"+url, callback=self.parse)


