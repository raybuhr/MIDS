#Kasane Utsumi
#storeNYTIntoDynamo.py
#New York Times articles are stored in one file per day. This python file takes begining day and end day as an argument and open json file for each day and saves content into DynamoDb

from boto.dynamodb2.table import Table
from boto.dynamodb2.layer1  import DynamoDBConnection
from boto.dynamodb2.items   import Item

import boto

import os
import logging
import sys
import json
import dateutil.parser
import time
from datetime import datetime
import dateutil
from datetime import timedelta
import codecs
import signal

#handle interrupt gracefully
def interrupt(signum, frame):
   print "Interrupted, closing ..."
   exit(1)

#Log so when error happenened, I can start from where I left off. 
logging.basicConfig(filename='dynamoDB'+ str(sys.argv[1]) + '.log',level=logging.DEBUG)

#get begin day to get articles from 
beginning = sys.argv[2]
beginningDay = dateutil.parser.parse(beginning)

#get end day to get articles until 
end = sys.argv[3]
endDay = dateutil.parser.parse(end)


#open dynamodb connection
try: 
	db=boto.dynamodb2.connect_to_region('us-west-2',aws_access_key_id='',aws_secret_access_key='')
except: 
	print "connect to dynamoDB failed! Exiting..."
	exit()

nyt = Table('NYT_NOSGI',connection=db)


def replaceEmptyString2(doc):
	for item in doc:
		#print item
		if type(doc[item]) is dict:
			if len(doc[item]) == 0:
				doc[item] = "EMPTY_TEXT"				
			doc[item] = replaceEmptyString2(doc[item])
		elif doc[item] == "":
			#print "empty found" 
			doc[item] = "EMPTY_TEXT"

                
	return doc


directory = os.getcwd() + "/articles"

articleCounter = 0

#keep opening nyt json files and saving until end day
while beginningDay <= endDay:
	articlePerDay = 0

	dayStr = str(beginningDay.strftime("%Y%m%d"))
	logging.debug("processing " + dayStr)
	
	filer=None

  	try:

		filer = codecs.open(directory +"/nyt-" + dayStr + ".json", "rb", encoding="utf-8")

	except:
	        logging.debug("could not open file" + filename)
		exit()
	
        data = json.loads(filer.read())

	filer.close()


	for dayArticle in data: #for each day
			if (dayArticle["response"] != None):
				#articles are bundled in group of 10 (because that is how much article per request NYT API was returning. 
	                        # will batch write for better performance and thoroughput saving. 
				with nyt.batch_write() as batch:

					for doc in dayArticle["response"]['docs']:
						logging.debug("processing articleId " + doc['_id'] + " published at " + doc['pub_date'])
		
						#must replace all empty string b/c otherwise dynamodb complains
						doc = replaceEmptyString2(doc)

				
						convertedDate = dateutil.parser.parse(doc['pub_date'])
		
						#saving datetime as timestamp
						timestamp = time.mktime((convertedDate.year, convertedDate.month, convertedDate.day,convertedDate.hour, convertedDate.minute, convertedDate.second,-1, -1, -1)) + convertedDate.microsecond / 1e6

						data = {
							"id"     : doc['_id'],
							"timestamp"     : timestamp,
						}

						data["headline"]  = replaceEmptyString2(doc['headline'])

						if (doc['news_desk'] !=  ""):
							data['type'] = doc['news_desk']
						if (doc['abstract'] !=  ""):
							data['abstract'] = doc['abstract']
						if (doc['lead_paragraph'] !=  ""):
							data['lead'] = doc['lead_paragraph']
						if (doc['snippet'] !=  ""):
							data['snippet'] = doc['snippet']
						if (doc['web_url'] !=  ""):
							data['web_url'] = doc['web_url']
						data['word_count'] = doc['word_count']
						data['source'] = doc['source']
						data['section_name'] = doc['section_name']
						data['pub_date'] = doc['pub_date']

						batch.put_item(data=data)

	logging.debug("total article for  " + dayStr + " was " + str(articlePerDay))
	beginningDay = beginningDay + timedelta(days=1)




exit()


