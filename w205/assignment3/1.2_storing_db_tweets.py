import sys
import datetime
import json
import pymongo
from boto.s3.connection import S3Connection

# AWS S3 connection
conn = S3Connection('AWS KEY', 'AWS SECRET')
myBucket = conn.get_bucket('rbuhr-tweets') 

# Get names of JSON files from assignment 2 stored in AWS S3 bucket
# add those names to a list to iterate over later
s3files = []
for key in myBucket:
<<<<<<< HEAD
	s3files.append(str(key.name))
=======
    s3files.append(str(key.name))
>>>>>>> 5ba6343218b2c08c3f25266aab278c757a52db6e

# Pull JSON files from assignment 2
for key in myBucket.list():
    try:
        result = key.get_contents_to_filename(key.name)
    except:
        logging.info(key.name+":"+"FAILED")

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
db = conn.db_tweets
collection = db.tweets


# Insert JSON into the database db_tweets
for filename in s3files:
<<<<<<< HEAD
	# Loop through each file from S3
	with open(filename) as json_filename:
		json_file = json.load(json_filename)
	for json_data in json_file:
		# Loop through each JSON object and insert into db_tweets
		collection.insert(json_data)

=======
    # Loop through each file from S3
    with open(filename) as json_filename:
        json_file = json.load(json_filename)
    for json_data in json_file:
        # Loop through each JSON object and insert into db_tweets
        collection.insert(json_data)
>>>>>>> 5ba6343218b2c08c3f25266aab278c757a52db6e
