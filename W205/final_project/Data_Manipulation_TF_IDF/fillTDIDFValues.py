# -*- coding: utf-8 -*-
#Kasane Utsumi - 05/02/2015
#fillTDIDFValues.py
#Fill Tf-Idf table with Tf-Idf value for a given keyword (passed as argv) for each articles in a given source
#For example, if keyword "obama" is passed, and DailyBeast is specified as a source, it calculate Tf-Idf for every article in DailyBeast table that contains a word "obama" and adds row to the  "TfIdfNew" table

#takes following argv
#1 - name of table that has count for all of the words in a given source. 
#2 - keyword to calculate tdidf
#3 - name of table that has body content for the data to calculate td idf from. 
#4 - name of the column from table above that has body of the text
#5 - name of the column from table above that has id for that entry, we will need to save id in the tdidf table
#6 - starting count for unique id that will be put into the tdidf table

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
from boto.dynamodb.condition import *
import TfIdf
from decimal import *
import signal

#handle interrupt gracefully
def interrupt(signum, frame):
   print "Interrupted, closing ..."
   exit(1)




db=boto.dynamodb2.connect_to_region('us-west-2',aws_access_key_id='',aws_secret_access_key='')


#get table with count of docs that contain a keyword
#table name is passed from the argv
#keyword is passed from argv

#"DailyBestSingleCount"
countTableName = sys.argv[1]
tableWithCount = Table(countTableName,connection=db)

keyword = sys.argv[2]

try:
	keywordRow = tableWithCount.get_item(word=keyword)
	numDocsWithKeyword = keywordRow['count']
except:
	print "keyword does not exist in this source. Try another one"
	exit()

print "num doc with keyword" +  str(numDocsWithKeyword)
	
#now get a table with documents
#"DailyBeast"
tablenameWithDocs = sys.argv[3]

tableWithDocs = Table(tablenameWithDocs,connection=db)

#get count of number of documents
#we know that this number gets updated only once every 6 hours. This would need to be modified if we are going to work with system in which articles are being added to the database 
#constantly
lengthOfCorpus = tableWithDocs.count()

#tableWithDocs.query_count(last_name__eq='Doe')

#rows = tableWithDocs.scan(body__contains= 'obama')
#index = 0
#for row in rows:
#	index +=1
#print index
#exit()

tdIdfCalculator = TfIdf.TfIdf(lengthOfCorpus,numDocsWithKeyword,keyword)

columnWithBody = sys.argv[4]

columnWithUniqueId = sys.argv[5]

rows = tableWithDocs.scan()

#this is the table to store Tf-Idf value
tdidfIndexTable = Table('TfIdfNew',connection=db)

#tdidfTl = tdidfIndexTable.query_2(word__eq = 'obama')
#for row in tdidfTl:
#	print row['articleId']
#	print row['tdIdfRoundTo7']



#used as a primary key
# I must maintain unique Id on my own because DynamoDb doesn't have functionality to create unique Id for you. 
uniqueId = int(sys.argv[6])

#boto dynamo2 bug won't let us python float, thus rounding by 7 decimal points and multiple by 10^7
def roundDecimal(flt):
	return int(round(Decimal(flt),7) * 10000000)

row = rows.next()

tableRowCount = 1

#round to 6 decimal points so we can save to dynamodb (known bug)

while row != None:
	#write 25 rows at the time, saves thoroughput and improves performance
	batchIndex = 0

	try: 
		with tdidfIndexTable.batch_write() as batch:
			print "starting new batch"
			while (batchIndex != 25):	
	
				if (row == None):
					break
				
				#calculate Tf-idf
				tdIdfValue = tdIdfCalculator.Calculate(row[columnWithBody])
				articleId = row[columnWithUniqueId]
	
				#No need to add entry for tf-idf if keyword does not appear in the source at all. 
				if tdIdfValue > 0:
					data={
					     'id': uniqueId,
					     'word': keyword,
  					     'articleId': str(articleId),
     					     'source': tablenameWithDocs,
     					     'tdIdfRoundTo7': roundDecimal(tdIdfValue), #bug with dynamo2 won't let us store float, so must convert to an integer
					}
					batch.put_item(data=data)
	
					print("Saving uniqueId " + str(uniqueId) + " source is " + tablenameWithDocs + " " + str(articleId) + " tdidf " + str(tdIdfValue))
				        
					uniqueId += 1
					batchIndex +=1
					
				tableRowCount +=1
				print "table row" + str(tableRowCount) 
				
				#if tableRowCount == lengthOfCorpus-1:
				#	break
				try:			
					row = rows.next()
				except StopIteration:
					row = None
					print "breaking"
					
	except:
		print "writing to TdIdf table failed. Aborting.."
		exit()
print "finished"




