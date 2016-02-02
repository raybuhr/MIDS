import tweepy
import json;

# Don't forget to install tweepy
# pip install tweepy

consumer_key = "g7WaeKhJUdXERWi7TBG2ET1hc";
consumer_secret = "cfNMs6S91KcIJuuQkWmAMem8ogY99F1ZbZr83fMCkJupxNstdh";

access_token = "63479910-PPtHT52R6zjhaQFiGYJPSfYwOCnDUyxn9LGI7ffEI";
access_token_secret = "FkUmm1mhuIvoKMfEtlPG1bYqIBCQ3k4Cephf1cJCWta6K";

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

for tweet in api.search(q="mojang" or "minecraft"):
   print tweet.text