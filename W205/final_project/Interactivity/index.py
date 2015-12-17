#Kasane Utsumi 
#index.py
#Flask-driven web application used for interactive demo. 
#It supports two flows: 1. Recommend a news source based on a keyword and current news source a user reads
#2. Based on the keyword entered, it will output average subjectivity, polairty, lexical diversity and article count of all articles (in which keyword id relevant enough per Tf-Idf value) from each source in a bar chart format. Bar chart was created using D3. 

from flask import Flask
import boto
from boto.dynamodb2.table import Table
from boto.dynamodb2.layer1  import DynamoDBConnection
from boto.dynamodb2.items   import Item
from boto.dynamodb.condition import *
from flask import request
import CompareSources
import CompareSources2
from tabulate import tabulate
from flask import render_template
import json


app = Flask(__name__)

#It will calculate call CompareSources module to get average stat of each source and output as json so it can be processed on client side. 
def Compare(term,score):
    CNN = CompareSources.CompareSources(term,'CNN',score)
    DB = CompareSources.CompareSources(term,'DailyBeast',score)
    RS = CompareSources.CompareSources(term,'RollingStone',score)
    WP = CompareSources.CompareSources(term,'Washington_Post',score)
    SF = CompareSources.CompareSources(term,'SF_Gate',score)    

    returnJson = [CNN.serializeToJson(), DB.serializeToJson(),
		RS.serializeToJson(),
		WP.serializeToJson(),
		SF.serializeToJson()]
    return json.dumps(returnJson)


#input the source that you want as the reference (oldsource), a keyword and it will output a recommended news source
def Newsource(oldsource, term, score):
    
    #create classes for all sources
    CNN = CompareSources.CompareSources(term,'CNN',score)
    DB = CompareSources.CompareSources(term,'DailyBeast',score)
    RS = CompareSources.CompareSources(term,'RollingStone',score)
    WP = CompareSources.CompareSources(term,'Washington_Post',score)
    SF = CompareSources.CompareSources(term,'SF_Gate',score) 
    
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


#load index.html (main page for barchart comparing article stats)
@app.route("/")
def hello():
    return render_template('index.html')

#url that gets called to display bar chart of article source statistics.
#takes keyword typed in as an input 
#returns a json object
@app.route('/getKeywordStats', methods=['POST', 'GET'])
def get_keyword_stats():

     keyword = request.form['keyword'] 
     try:
	     #We are getting articles in which keyword is at least .001	(we are passing 1000 because b/c of boto dynamodb2 issues we had to multiply tfidf by 10^7 just to store in the database. 
	     return Compare(keyword,1000)
     except:
	     return {"error": "Error happened. Please contact an admin." }      

#load recommend home page (main page for article recommender)
@app.route('/recommendHome', methods=['POST', 'GET'])
def recommender():
    return render_template('recommend.html')

#url that gets called to display recommended source.
#takes keyword and article source one currently reads, typed in as input 
#returns a string (name of a recommended source)
@app.route('/recommend', methods=['POST', 'GET'])
def recommend():
    keyword = request.form['keyword'] 
    source = request.form['source']

    try:
	    return Newsource(source,keyword,1000)
    except: 
	    return "Sorry, error happened and we could not find a source for you." 

if __name__ == "__main__":
	app.run(debug=True)
