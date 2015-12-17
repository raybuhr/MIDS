# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 12:27:20 2015

@author: Julian
"""

import boto.dynamodb2

from boto.dynamodb2.table import Table
import arrow
from tabulate import tabulate

class CompareSources:
    def __init__(self,term,database,score):
        
        #create variables for storing data of interest
        self.lexdiv =[]
        self.subjectivity=[]
        self.polarity=[]
        #put both maxdate and mindate in formats that can be compared to later with dates outside the range
        self.origmaxdate=arrow.now().replace(years=-5)
        self.maxdate=self.origmaxdate.format('YYYY-MM-DD HH:mm')
        self.origmindate=arrow.now()  
        self.mindate=self.origmindate.format('YYYY-MM-DD HH:mm')
        self.articleIDs=[]
        self.term=term
        self.source=database
        self.score=score
        self.articleIDsub=[]
        self.IDtracker=[]
        self.dayscount={}
        #tables times are stored differently.  This dictionary contains all possibilties and the correct one is selected using
        #self.source as a key
        self.dtstringdict= {'DailyBeast': "MM-DD-YY h:mm", 'CNN':"MMM-D-YYYY h:mm","Huffington_Post":"YYYY-MM-DD HH:mm:ss","Washington_Post":"YYYY-MM-DD HH:mm:ss"
                        ,"RollingStone":"YYYY-MM-DD HH:mm:ssZZ","SF_Gate":"YYYY-MM-DD HH:mm:ss"}        
        self.dtstring = self.dtstringdict[self.source]
        
        #table indices are stored differently.  This dictionary contains all possibilties and the correct one is selected using
        #self.source as a key
        self.indexdict= {'DailyBeast': "tstamp", 'CNN':"tstamp","Huffington_Post":"id","Washington_Post":"id"
                        ,"RollingStone":"id","SF_Gate":"id"}        
        self.index = self.indexdict[self.source]
        
        #the name of columns that have dates are different.  This dictionary selects the correct one.
        
        self.dtdict= {'DailyBeast': "datetime", 'CNN':"datetime","Huffington_Post":"date","Washington_Post":"date"
                        ,"RollingStone":"date","SF_Gate":"date"}         
        self.dtstr = self.dtdict[self.source]
        
        #These data sources were set up without a RangeKey on Dyanmo.  Therefore to use batch get, there is a slightly
        #different syntax that needs to be used.  A later if/then statement does thsis.
        self.norangesources = ["Huffington_Post","Washington_Post", "RollingStone","SF_Gate"]
        
        #connect to dynamodb
        conn = boto.dynamodb2.connect_to_region(
        'us-west-2',
        aws_access_key_id='',
        aws_secret_access_key='')
        
        
        #Create table variables.  
        table = Table(self.source, connection=conn)
        querytable=Table('IndexTdIdf',connection=conn)
        
        #Collect all articleIDs from IndexTDIDF table that match the term given and the desired score
        #puts in dictionaries of 100 for batch get in a list
        
        for row in querytable.scan():
            if row["word"]==self.term and row["source"]==self.source and row["tdIdfRoundTo7"] > self.score and int(float(row["articleId"])) not in self.IDtracker:
                #this is the code where some  take hash and range key and others just hash key to do batch get
                if self.source in self.norangesources:
                    dictvalue = {self.index:int(float(row["articleId"]))}
                else:    
                    dictvalue = {self.index:int(float(row["articleId"])),'source':self.source}
                self.articleIDsub.append(dictvalue)
                self.IDtracker.append(int(float(row["articleId"])))
                if len(self.articleIDsub) == 100:
                    self.articleIDs.append(self.articleIDsub)
                    self.articleIDsub = []
                else:
                    continue
        #make to append any left over that is not in a group of 100
        self.articleIDs.append(self.articleIDsub)
      
        for entry in self.articleIDs:            
            results = table.batch_get(keys=entry)       
            for result in results:
                if result[self.dtstr] is not None or '':
                    try:
                        tm = arrow.get(result[self.dtstr], self.dtstring)
                        tm=tm.format('YYYY-MM-DD')
                    except:
                        continue
                
                    if tm in self.dayscount.keys():
                        self.dayscount[tm]+=1
                    else:
                        self.dayscount[tm]=1
                
                    if tm > self.maxdate:
                        self.maxdate = result[self.dtstr]
                    if tm < self.mindate:
                        self.mindate = result[self.dtstr]                
                
                
                
                
                if (result['lexical diversity']) is not None or 0:
                    self.lexdiv.append(result['lexical diversity'])
                    
                if (result["subjectivity"]) is not None or 0:
                    self.subjectivity.append(result["subjectivity"])   
                    
                if (result["polarity"]) is not None or 0:
                    self.polarity.append(result["polarity"])  
                    
                
            
        
                
    def subjectivity_value(self):
        if len(self.subjectivity)==0:
            return 0
        else:
            return round(sum(self.subjectivity)/len(self.subjectivity),3)
           
    def polarity_value(self):
        if len(self.polarity)==0:
            return 0
        else:
            return round(sum(self.polarity)/len(self.polarity),3)
            
    def lexdiv_value(self):
        if len(self.lexdiv)==0:
            return 0
        else:
            return round(sum(self.lexdiv)/len(self.lexdiv),2)
            
    def total(self):
        return len(self.lexdiv)
    
    def maxdate_value(self):
        if self.maxdate == self.origmaxdate:
            return "N/A"
        else:
            self.maxdate= arrow.get(self.maxdate, self.dtstring)
            return self.maxdate.format('YYYY-MM-DD')
        
    def mindate_value(self):
        if self.mindate == self.origmindate:
            return "N/A"
        else:
            self.mindate= arrow.get(self.mindate, self.dtstring)
            return self.mindate.format('YYYY-MM-DD')
    
    def dayscount_value(self):
        return self.dayscount
        
    def source_value(self):
        return self.source
        
    def serializeToJson(self):
        
        return { 
                "Label": self.source,
                "Total": self.total(),
                "LexicalDiversity": self.lexdiv_value(),
                "Polarity": self.polarity_value(),
                "Subjectivity": self.subjectivity_value()
                }
        
        
        
        
        
        
        
      
        


#Can create a table showing differences.  Not being used at the moment.
def Compare(term,score):
    CNN = CompareSources(term,'CNN',score)
    DB = CompareSources(term,'DailyBeast',score)
    RS = CompareSources(term,'RollingStone',score)
    WP = CompareSources(term,'Washington_Post',score)
    SF = CompareSources(term,'SF_Gate',score) 
    
    table =[["Number of Articles",CNN.total(),DB.total(),CNN.total(),RS.total(),WP.total(),SF.total()],
            ["Lexical Diversity",CNN.lexdiv_value(),DB.lexdiv_value(),RS.lexdiv_value(),WP.lexdiv_value(),SF.lexdiv_value()],
            ["Polarity",CNN.polarity_value(),DB.polarity_value(),RS.polarity_value(),WP.polarity_value(),SF.polarity_value()],
            ["Subjectivity",CNN.subjectivity_value(),DB.subjectivity_value(),RS.subjectivity_value(),WP.subjectivity_value(),SF.subjectivity_value()],
            ["Earliest Article",CNN.mindate_value(),DB.mindate_value(),RS.mindate_value(),WP.mindate_value(),SF.mindate_value()],
            ["Latest Article",CNN.maxdate_value(),DB.maxdate_value(),RS.maxdate_value(),WP.maxdate_value(),SF.maxdate_value()]]
    print tabulate(table)
    





#input the source that you want as the reference (oldsource), the term for comparison and the score threshold you are intersted in
def Newsource(oldsource, term, score):
    
    #create classes for all sources
    CNN = CompareSources(term,'CNN',score)
    DB = CompareSources(term,'DailyBeast',score)
    RS = CompareSources(term,'RollingStone',score)
    WP = CompareSources(term,'Washington_Post',score)
    SF = CompareSources(term,'SF_Gate',score) 
    
    #Match the original source
    if oldsource == "RollingStone":
        oldsource = RS
    if oldsource == "DailyBeast":
        oldsource = DB
    if oldsource == "CNN":
        oldsource = CNN
    if oldsource == "Washington_Post":
        oldsource = WP
    if oldsource == "SF_Gate":
        oldsource = SF
     
    origsources = [RS,DB,CNN,WP,SF]
    sources=[]
     
    for source in origsources:
        if source <> oldsource:
            sources.append(source)         
    
        
#comparison is just pct difference between the old and new.  will add complexity in future versions
    def comparesrces(first, second):
        
        lexdivdiff = abs((second.lexdiv_value()-first.lexdiv_value())/first.lexdiv_value())
        poldiff = abs((second.polarity_value()-first.polarity_value())/first.polarity_value())
        subdiff = abs((second.subjectivity_value()-first.subjectivity_value())/first.subjectivity_value())
        totaldiff = lexdivdiff+poldiff+subdiff        
        return totaldiff
        
    low=100
    
    for src in sources:
        val = comparesrces(oldsource,src)
        
        if val < low:
            low=val
            newsrce=src.source_value()    
        
        
    return newsrce



 
    
    
    
    








