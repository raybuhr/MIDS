# -*- coding: utf-8 -*-
import sys
import tweepy
import datetime
import urllib
import signal
import json
import pymongo

# Connection to Mongo DB
try:
<<<<<<< HEAD
	conn=pymongo.MongoClient()
	print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
	print "Could not connect to MongoDB: %s" %e 
=======
    conn=pymongo.MongoClient()
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" %e 
>>>>>>> 5ba6343218b2c08c3f25266aab278c757a52db6e

# creating mongodb database
db = conn.db_streamT
collection = db.tweets

# Twitter authorization
consumer_key = "...";
consumer_secret = "...";
access_token = "...";
access_token_secret = "...";

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

# define interrupt handler in case need to shutdown data collection
def interrupt(signum, frame):
<<<<<<< HEAD
	print "Interrupted, closing ..."
	# magic goes here
	exit(1)
=======
    print "Interrupted, closing ..."
    # magic goes here
    exit(1)
>>>>>>> 5ba6343218b2c08c3f25266aab278c757a52db6e
signal.signal(signal.SIGINT, interrupt)

# tweepy search builder
q = urllib.quote_plus(sys.argv[1]) # URL encoded query
start_day = str(sys.argv[1]) # enter start date in terminal as yyyy-mm-dd
end_day = str(sys.argv[2]) # enter end date in terminal as yyyy-mm-dd
q = q + " since:"+start_day+" until:"+end_day # create query from system args

# run the search and store JSON to mongoDB db_streamT, collection tweets
for tweet in tweepy.Cursor(api.search,q=q,lang="en").items():
    data ={}
    data['created_at'] = tweet.created_at
    data['text'] = tweet.text
    data['id'] = tweet.id
    data['retweeted'] = tweet.retweeted
    data['in_reply_to_user_id'] = tweet.in_reply_to_user_id
    data['in_reply_to_screen_name'] = tweet.in_reply_to_screen_name
    data['retweet_count'] = tweet.retweet_count
    data['geo'] = tweet.geo
    data['coordinates'] = tweet.coordinates
    collection.insert(data) #insert data to mongodb
    print data #show api returns in terminal
<<<<<<< HEAD
    
    
=======
>>>>>>> 5ba6343218b2c08c3f25266aab278c757a52db6e
