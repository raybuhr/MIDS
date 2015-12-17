#!/usr/bin/python

'''
First need to scrape Daily Beast articles
In command line:
  scrapy startproject beastCrl
  cp ./DailyBeastscrapyInputs/items.py ./beastCrl/beastCrl/
  cp ./DailyBeastscrapyInputs/test.py ./beastCrl/beastCrl/spiders/
  cd beastCrl
  scrapy crawl beastCrl -o beastCrl.json -t json

Then run in command line:
  ../DailyBeast_scraper.py
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

def removeDuplicates_beast(beastjson):
  ''' Remove duplicate documents from scraped data '''
  dedupedj = []
  titles = {}
  for article in j:
    if not article['title'] in titles:
      dedupedj.append(article)
      titles[article['title']]=True
    else:
      continue
  return dedupedj



def soup_beast(beastjson):
  ''' Clean up scraped data from Daily Beast '''
  prettybeast = []
  for article in beastjson:
    entry = {}
    entry["body"] = bs4.BeautifulSoup(article["body"]).get_text()
    entry["title"] = bs4.BeautifulSoup(article["title"]).get_text()
  
    soupdate = bs4.BeautifulSoup(article["datetime"])
    datetimelist = [str(soupdate.find_all("span")[0].get_text()),str(soupdate.find_all("span")[1].get_text())]
    datetimestr = ' '.join(datetimelist).replace('.','-')
    #print "datetime is "+datetimestr
    #print '\n'
    #print article["datetime"]
    #print datetimestr
    try:
      convertedDate = dateutil.parser.parse(datetimestr)
      temp = time.mktime((convertedDate.year, convertedDate.month, convertedDate.day, convertedDate.hour, convertedDate.minute, convertedDate.second, -1, -1, -1)) + convertedDate.microsecond / 1e6
      entry["datetime"]=datetimestr
      entry["timestamp"]=str(temp)
      prettybeast.append(entry)
    except:
      #entry["datetime"]="NA"
      #entry["timestamp"]="NA"
      continue

  return prettybeast


def tstampdedup_beast(beastjson):
  ''' Add small increment to articles that have same timestamp to avoid collisions in DynamoDB range keys '''
  
  dedupedj = []
  tstamps = {}
  for article in beastjson:
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


def sendtodynamo_beast(beastjson):
  ''' Send json to DynamoDB
  Assumes that article timestamps have been deduped to avoid collisions
  '''

  conn = connect_to_region('us-west-2', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
  
  hashkey = "DailyBeast" # primary key to be used for DynamoDB table

  try:
    table = Table('DailyBeast', connection=conn)
    table.describe()
  except boto.exception.JSONResponseError:
    print "Creating table"
    table = Table.create('DailyBeast', schema=[HashKey('source'), RangeKey('tstamp',data_type=NUMBER)], throughput={'read':25, 'write':25})

  iteration = 0
  for article in beastjson:
    # Iterate through list of articles and upload to table
    rangekey = float(article['timestamp'])
    rowdata = {'source':hashkey,'tstamp':rangekey}
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
    copy_to_s3('beastCrl.json')
  except:
    print "Backup to S3 failed. Skipped."
  
  # load scraped data json
  try:
    f = open("./beastCrl.json", 'r')
  except:
    print "Couldn't open json. Exitiing."
    sys.exit()

  lines = f.readlines()
  beastjson = json.loads(''.join(lines))
  print "loaded jsons"


  # remove duplicate articles from scraped data
  deduped_beastjson = removeDuplicates_beast(beastjson)


  # use Beautiful soup to clean up scraped data
  prettybeast = soup_beast(deduped_beastjson)
  print "prettified"

  # Add small increment to articles that have same timestamp to avoid collisions in DynamoDB range keys
  deduped_prettybeast = tstampdedup_beast(prettybeast)
  print "deduped"

  # Upload DailyBeast articles to DynamoDB
  sendtodynamo_beast(deduped_prettybeast)

