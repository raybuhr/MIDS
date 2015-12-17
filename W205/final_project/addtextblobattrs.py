# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 16:30:16 2015

@author: Julian
"""
import boto
import boto.dynamodb
from textblob import TextBlob


def update(table, field): 
    conn = boto.dynamodb.connect_to_region(
        'us-west-2',
        aws_access_key_id='',
        aws_secret_access_key='')   
    table = conn.get_table(table)       
    for line in table.scan():
        newline =line[field]
        text=TextBlob(newline) 
        text = text.lower()
        textwords = text.split()
        wordcount = 0
        wordlist = []
        for word in textwords:
            wordcount +=1
            if word not in wordlist:
                wordlist.append(word)
                #handles div0 errors
        if wordcount ==0:
            lexdiv =0
        else:
            lexdiv =round((len(wordlist)*1.0)/wordcount,2)
     
        polarity=text.sentiment.polarity
        subjectivity=text.sentiment.subjectivity    
        line.put_attribute('subjectivity',subjectivity) 
        line.put_attribute('polarity',polarity)
        line.put_attribute('lexical diversity',lexdiv)
        line.save()
        
                            
update('CNN','body')
