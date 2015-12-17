# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 10:07:03 2015

@author: julian
"""

import tweepy;
import json;
import sys
import time
from os import walk
import os
import boto.dynamodb
import shutil  

consumer_key = "XXX";
consumer_secret = "XXX";

access_token = "XXX";
access_token_secret = "XXX";

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

API = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):
    def __init__(self):
        self.counter = 0
        self.totalcounter =0
        self.fprefix = 'streamer'
        self.output  = open('streaming_data/'+self.fprefix + '.' 
                            + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
                            
    def on_data(self, data):
        if  'in_reply_to_status' in data:
            self.on_status(data)        

    def on_status(self, status):
        self.output.write(status)

        self.counter += 1
        
        if self.totalcounter == 10:
            sys.exit()
        
        if self.counter >= 20000:
            self.output.close()
            self.output = open('streaming_data/' + self.fprefix + '.' 
                               + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
            self.counter = 0
            self.totalcounter +=1

        return

    
    def on_limit(self, track):
        sys.stderr.write(track + "\n")
        return

    def on_error(self, status_code):
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return False

    def on_timeout(self):
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return 
 
    
        
localdir = "C:/MIDS/W205/205FinalProject"      
moveddir = "C:/MIDS/W205/205FinalProject/oldstreamingdata"           

       
def uploadtweets(): 
    conn = boto.dynamodb.connect_to_region(
        'us-west-2',
        aws_access_key_id='XXX',
        aws_secret_access_key='XXX')
    table = conn.get_table('twitter')
    for (dirpath,dirname,filenames)in walk(localdir+'/streaming_data'):
        for filename in filenames:
            workingfile= localdir+'\streaming_data/'+filename
            jsontweets = open(workingfile,"r")
            hashkey = int(filename[9:17]+filename[18:24])*10000
            for tweet in jsontweets:
                try:
                    tweet = json.loads(tweet)                    
                    if tweet.get("lang",None) <> 'en':
                        continue                    
                    else:
                        ts = time.strftime('%Y%m%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
                        item_data = {
                        'Body': tweet["text"],
                        'Source': 'Twitter',
                        'Date': ts,
                        }
                        item=table.new_item(hash_key = str(hashkey),attrs=item_data)
                        item.put()
                        hashkey +=1 
                        print hashkey                        
                except ValueError:
                    continue
            print workingfile
            jsontweets.close()
            shutil.move(workingfile, moveddir)
                
                

sapi = tweepy.Stream(auth, CustomStreamListener())
sapi.sample()
uploadtweets()






