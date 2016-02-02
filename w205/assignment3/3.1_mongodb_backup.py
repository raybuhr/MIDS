'''
3.1­ Write a python program to create and store the backups of both db_tweets and
db_streamT to S3. It also should have a capability of loading the backups if necessary.
'''
import pymongo
import os.path
import sys
import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from os.path import join
from bson.json_util import dumps
from bson.json_util import loads

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

db_tweets = conn.db_tweets
db_streamT = conn.db_streamT

# function that iterates through collections in a mongo db and stores as bson
def backup_db(db, backup_path):
    collections = db.collection_names()
    for i, collection_name in enumerate(collections):
        col = getattr(db,collections[i])
        collection = col.find()
        jsonpath = collection_name + ".json"
        jsonpath = join(backup_path, jsonpath)
        with open(jsonpath, 'wb') as jsonfile:
            jsonfile.write(dumps(collection))

# set location for backups
backup_path = "/db_backup/"
# use backup_db function to backup databases
backup_db(db_tweets, backup_path + "db_tweets") 
backup_db(db_streamT, backup_path + "db_streamT")

# store those backups to S3
# AWS S3 connection
connS3 = S3Connection('AWS_KEY', 'AWS_SECRET')
myBucket = connS3.get_bucket('w205-3-asgn3-rbuhr') 

# little function to show progress
def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()
 
# function that loops through file names in path and uploads to S3 bucket
def s3_db_upload(path, folder):
<<<<<<< HEAD
	# get list of file names in path
	fileNames = []
	for (path, dirname, filename) in os.walk(path):
		fileNames.extend(filename)
	# folder S3 bucket to upload
	destination = folder
	for filename in uploadFileNames:
		sourcepath = os.path.join(path +'/'+ filename)
		destpath = os.path.join(destination, filename)
		print 'Uploading %s to Amazon S3 bucket' %(sourcepath)
		k = Key(myBucket)
		k.key = destpath
		k.set_contents_from_filename(sourcepath, cb=percent_cb, num_cb=10)
=======
    # get list of file names in path
    fileNames = []
    for (path, dirname, filename) in os.walk(path):
        fileNames.extend(filename)
	# folder S3 bucket to upload
    destination = folder
    for filename in uploadFileNames:
        sourcepath = os.path.join(path +'/'+ filename)
        destpath = os.path.join(destination, filename)
        print 'Uploading %s to Amazon S3 bucket' %(sourcepath)
        k = Key(myBucket)
        k.key = destpath
        k.set_contents_from_filename(sourcepath, cb=percent_cb, num_cb=10)
>>>>>>> 5ba6343218b2c08c3f25266aab278c757a52db6e

# use s3_db_upload function to store backups in cloud
s3_db_upload(backup_path+'db_tweets/','db_tweets')
s3_db_upload(backup_path+'db_streamT/', 'db_streamT')

# function to restore from bson files
def build_db(db_name):
<<<<<<< HEAD
	# connect to S3 and download backups
	s3files = []
	for key in myBucket:
		s3files.append(str(key.name))
	for key in myBucket.list():
    	try:
        	result = key.get_contents_to_filename(key.name)
    	except:
        	logging.info(key.name+":"+"FAILED")
	# connect to mongoDB
	conn = pymongo.MongoClient()
	db = conn.db_name
	# Loop through each file from S3
	for filename in s3files:
		collection = db.filename
		with open(filename) as bson_filename:
			bson_file = load(bson_filename)
		for bson_data in bson_file:
		# Loop through each BSON object and insert into mongoDB
			collection.insert(bson_data)
=======
    # connect to S3 and download backups
    s3files = []
    for key in myBucket:
        s3files.append(str(key.name))
    for key in myBucket.list():
        try:
            result = key.get_contents_to_filename(key.name)
        except:
            logging.info(key.name+":"+"FAILED")
	# connect to mongoDB
    conn = pymongo.MongoClient()
    db = conn.db_name
    # Loop through each file from S3
    for filename in s3files:
        collection = db.filename
        with open(filename) as bson_filename:
            bson_file = load(bson_filename)
        for bson_data in bson_file:
        # Loop through each BSON object and insert into mongoDB
            collection.insert(bson_data)
>>>>>>> 5ba6343218b2c08c3f25266aab278c757a52db6e
