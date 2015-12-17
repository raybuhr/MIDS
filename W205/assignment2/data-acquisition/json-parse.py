import sys
import re
import json
import pandas as pd


raw_objs_string = open('twitter_data-'+str(sys.argv[1])+'.txt').read() #read in raw data
raw_objs_string = raw_objs_string.replace('}{', '},{') #insert a comma between each object
objs_string = '[%s]'%(raw_objs_string) #wrap in a list, to make valid json
objs = json.loads(objs_string) #parse json

tweet = objs[0]
ids = []
for tweet in objs:
  ids.append(tweet['id_str'])
  
ids = [tweet['id_str'] for tweet in objs]
texts = [tweet['text'] for tweet in objs]
times = [tweet['created_at'] for tweet in objs]

tweets = pandas.DataFrame(texts)
daytweets = open(str(sys.argv[1])+'.txt', 'w')
tweets.to_csv(daytweets, encoding='utf-8')


'''
suggestion for converting twitter json to useable json from:
http://stackoverflow.com/a/8730769
'''
