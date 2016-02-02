import sys
import tweepy
import datetime
import urllib
import signal
import json

# Don't forget to install tweepy
# pip install tweepy

consumer_key = "g7WaeKhJUdXERWi7TBG2ET1hc";
consumer_secret = "cfNMs6S91KcIJuuQkWmAMem8ogY99F1ZbZr83fMCkJupxNstdh";

access_token = "63479910-PPtHT52R6zjhaQFiGYJPSfYwOCnDUyxn9LGI7ffEI";
access_token_secret = "FkUmm1mhuIvoKMfEtlPG1bYqIBCQ3k4Cephf1cJCWta6K";


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

q = urllib.quote_plus(sys.argv[1])  # URL encoded query

# Additional query parameters:
#   since: {date}
#   until: {date}
# Just add them to the 'q' variable: q+" since: 2014-01-01 until: 2014-01-02"
for tweet in tweepy.Cursor(api.search,q=q).items(200):
   # FYI: JSON is in tweet._json
   print tweet._json
