#Kasane Utsumi
#retrieveNYTArticles.py
#Use nytimesarticle package to retreive new york times articles. 
#key required to use NYT API is passed as first argument
#beginning day is passed as a second argument, and it will retrieve article until end of that month. 
#For example, if "03-22-2013" was passed as an argument, it will get articles from 03-22 until 03-31



from nytimesarticle import articleAPI
import json
import dateutil.parser
import time
from datetime import datetime
from datetime import timedelta
import sys
import logging
import signal

#handle interrupt gracefully
def interrupt(signum, frame):
   print "Interrupted, closing ..."
   exit(1)


logging.basicConfig(filename='example'+ str(sys.argv[2]) + '.log',level=logging.DEBUG)


import urllib
import sys

try:
	api = articleAPI(sys.argv[1])
except:
	print "could not open articleAPI library. Exiting..."
	exit()

#articles = api.search( q = 'Obama', fq = {'headline':'Obama', 'source':['Reuters','AP', 'The New York Times']}, begin_date = 20111231, facet_field = ['source','day_of_week'], facet_filter = True )


#articles = api.search(begin_date = 20150308,end_date = 20150314)
#print json.dumps(articles)

articleCount = 0

month = urllib.quote_plus(sys.argv[2])

beginningDay = dateutil.parser.parse(month)

currentMonth = beginningDay.month
newMonth = currentMonth

totalArticleCount = 0


#keep retrieving articles until next month
while newMonth == currentMonth:
	

	done = False
	pageIndex = 1
	logging.debug("getting articles on:" + str(beginningDay))


	fileName = "articles/nyt-" +str(beginningDay.strftime("%Y%m%d"))+".json"
        
	myFile = None
	try:
	      	myFile = open(fileName,"w+")
      	except:
        	logging.warning("opening file failed for " + fileName)
        
	myFile.write("[")
	isTheBeginning = True

	#store one day worth of articles in one file
	while not done:
		if pageIndex == 101:
			break
		
		try:		
	      		articles = api.search(begin_date = beginningDay.strftime("%Y%m%d"),end_date = beginningDay.strftime("%Y%m%d"),page=pageIndex)
		except:
			"Article retreival failed! Abort. It failed on these days" +  beginningDay.strftime("%Y%m%d") + beginningDay.strftime("%Y%m%d")

      		logging.debug("page is " + str(pageIndex))

		
		if not isTheBeginning:
         		myFile.write(",\n") 	
		isTheBeginning = False


      		myFile.write(json.dumps(articles))   
	
		totalArticleCount += len(articles['response']['docs']) 
      		if len(articles['response']['docs']) == 0: 
         		done = True    
      		pageIndex += 1

	myFile.write("]\n")
	myFile.close()

	beginningDay = beginningDay + timedelta(days=1)
	newMonth = beginningDay.month


logging.debug("articleCount: " + str(totalArticleCount))
