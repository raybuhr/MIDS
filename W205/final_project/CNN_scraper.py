#!/usr/bin/python

'''
First need to scrape CNN transcripts
In command line:
  scrapy startproject cnnCrl
  cp ./CNNscrapyInputs/items.py ./cnnCrl/cnnCrl/
  cp ./CNNscrapyInputs/test.py ./cnnCrl/cnnCrl/spiders/
  cd cnnCrl
  scrapy crawl cnnCrl -o cnnCrl_year.json -t json

Then run in command line:
  ../CNN_scraper.py
'''

import sys
import json
from pprint import pprint

import boto.dynamodb2
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER
from boto.dynamodb2 import connect_to_region

import bs4
import dateutil.parser
import time
from datetime import datetime


AWS_ACCESS_KEY_ID=''
AWS_SECRET_ACCESS_KEY=''
S3BUCKETNAME = ''


def copy_to_s3(filename):
  ''' Copy file to S3 bucket '''
  conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    
  bucketname = S3BUCKETNAME
  bucket = conn.create_bucket(bucketname)
    
  k = Key(bucket)
  k.key = filename
  k.set_contents_from_filename(filename)

  print 'Uploading %s to Amazon S3 bucket %s' %(filename, bucketname)

  return None


def soup_cnn(cnnjson):
  ''' Clean up scraped data from CNN '''
  prettycnn = []
  for article in cnnjson:
    entry = {}
    entry["body"] = bs4.BeautifulSoup(article["body"]).get_text()
    entry["subhead"] = bs4.BeautifulSoup(article["subhead"][0]).get_text()
    entry["show"] = bs4.BeautifulSoup(article["show"]).get_text()

    months = {"January":"Jan","February":"Feb","March":"Mar","April":"Apr","May":"May","June":"Jun","July":"Jul","August":"Aug","September":"Sep","October":"Oct","November":"Nov","December":"Dec"}

    datetimelist = bs4.BeautifulSoup(article["date"]).get_text().replace('Aired ','').replace('- ','').replace(u'\xa0','').replace(',','').replace('>','').split(' ')
    datetimestr = months[datetimelist[0]]+'-'+datetimelist[1]+'-'+datetimelist[2]+' '+datetimelist[3]+' '+datetimelist[5]

    try:
      convertedDate = dateutil.parser.parse(datetimestr)
      temp = time.mktime((convertedDate.year, convertedDate.month, convertedDate.day, convertedDate.hour, convertedDate.minute, convertedDate.second, -1, -1, -1)) + convertedDate.microsecond / 1e6
      entry["datetime"]=datetimestr
      entry["timestamp"]=str(temp)
    except:
      continue
    
    #print "timestamp is " + str(temp)
    #print "checking to see if converting to timestamp worked by reversing it" + str(datetime.fromtimestamp(temp))

    prettycnn.append(entry)
    if len(prettycnn)%100==0:
      print len(prettycnn)

  return prettycnn


def tstampdedup_cnn(cnnjson):
  ''' Clean up scraped data from CNN '''
  
  dedupedj = []
  tstamps = {}
  
  for article in cnnjson:
    floattime = float(article['timestamp'])
    if not article['timestamp'] in tstamps:
      tstamps[article['timestamp']]=0.0
    else:
      tstamps[article['timestamp']]+=1.0
      #print '\n'
      #print article['timestamp']
      #print 0.0001*tstamps[article['timestamp']]
      article['timestamp'] = "{:14.3f}".format(floattime+0.001*tstamps[article['timestamp']])
      #print article['timestamp']
      #print article['datetime']
    dedupedj.append(article)

    if len(dedupedj)%100==0:
      print len(dedupedj)

  return dedupedj


def sendtodynamo_cnn(cnnjson):
  ''' Send json to DynamoDB
  Assumes that article timestamps have been deduped to avoid collisions
  '''

  conn = connect_to_region('us-west-2', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
  
  hashkey = "CNN" # primary key to be used for DynamoDB table

  try:
    table = Table('CNN', connection=conn)
    table.describe()
  except boto.exception.JSONResponseError:
    print "Creating table"
    table = Table.create('CNN', schema=[HashKey('source'), RangeKey('tstamp',data_type=NUMBER)], throughput={'read':25, 'write':25}, indexes=[GlobalAllIndex('showidx',parts=[HashKey('show')],throughput={'read':10,'write':5})])

  iteration = 0
  for article in cnnjson:
    # Iterate through list of articles and upload to table
    rangekey = float(article['timestamp'])
    rowdata = {'source':hashkey,'tstamp':rangekey, 'cnnShow':article['show']}
    for key in article.keys():
      rowdata[key]=article[key]
    item = table.put_item(data = rowdata)
    iteration += 1
    if iteration%100==0:
      print "Uploaded "+iteration+" articles"

  return None



if __name__ == '__main__':

  # backup scraped data to S3
  try:
    copy_to_s3('cnnCrl_test.json')
  except:
    print "Backup to S3 failed. Skipped."
  
  # load scraped data json
  try:
    f = open("./cnnCrl_test.json", 'r')
  except:
    print "Couldn't open json. Exitiing."
    sys.exit()

  lines = f.readlines()
  cnnjson = json.loads(''.join(lines))
  print "loaded jsons"

  # use Beautiful soup to clean up scraped data
  prettycnn = soup_cnn(cnnjson)
  print "prettified"

  # Add small increment to articles that have same timestamp to avoid collisions in DynamoDB range keys
  deduped_prettycnn = tstampdedup_cnn(prettycnn)
  print "deduped"

  # Upload CNN transcripts to DynamoDB
  sendtodynamo_cnn(deduped_prettycnn)

