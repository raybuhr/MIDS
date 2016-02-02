# -*- coding: utf-8 -*-
import sys
import tweepy
import datetime
import urllib
import signal
import json
from boto.s3.connection import S3Connection

# Twitter auth
consumer_key = "g7WaeKhJUdXERWi7TBG2ET1hc"
consumer_secret = "cfNMs6S91KcIJuuQkWmAMem8ogY99F1ZbZr83fMCkJupxNstdh"
access_token = "63479910-PPtHT52R6zjhaQFiGYJPSfYwOCnDUyxn9LGI7ffEI"
access_token_secret = "FkUmm1mhuIvoKMfEtlPG1bYqIBCQ3k4Cephf1cJCWta6K"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

# AWS S3 connection
conn = S3Connection('AKIAIRFWKMQG66FFWRCA', 'l/6tj4d166P6Gw5duZxuMcq6A5yHjZbXr/f0utlK')
myBucket = conn.get_bucket('rbuhr-tweets') 

class TweetSerializer():
    out = None
    first = True
    count = 0
    def start(self):
        count += 1
        fname = "tweets-"+str(count)+".json"
        self.out = open(fname,"w")
        self.out.write("[\n")
        self.first = True

    def end(self):
        if self.out is not None:
            self.out.write("\n]\n")
            self.out.close()
        self.out = None

    def write(self,tweet):
        if not self.first:
            self.out.write(",\n")
        self.first = False
        self.out.write(json.dumps(tweet._json).encode('utf8'))

# Twitter search query
#q = urllib.quote_plus(sys.argv[1])
# URL encoded query

# TODO: figure out a way to loop through 7 days
# For now: replace next day and run script again
day1 = str(sys.argv[1])
day2 = str(sys.argv[2])
q = "#minecraft OR #mojang since:"+day1+" until:"+day2


for tweet in tweepy.Cursor(api.search,q=q,lang="en").items():
#    FYI: JSON is in tweet._json
#    TweetSerializer.start()
#    TweetSerializer.write(tweet)
#    TweetSerializer.end()
#    could not get tweet serializer class to work, got this error:
#    unbound-method-operate-must-be-called-with-instance-as-first-argument
#	write json to file
    print tweet._json
    file_name = 'twitter_data-'+day1+'.txt'
    twitter_data = open(file_name,'a')
    twitter_data.write(json.dumps(tweet._json).encode('utf8'))
    
# upload json to s3 bucket
def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()
from boto.s3.key import Key
k = Key(myBucket)
k.key = file_name
k.set_contents_from_filename(file_name, cb=percent_cb, num_cb=10)

