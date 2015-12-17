'''
Retrieving and Analyzing Task 2.1
Step 1: Find the top 30 retweets from assignment 2
Step 2: Find the associated usernames of the top 30 retweets
Step 3: Find the location of the users who retweeted
'''
import pymongo

# Connection to Mongo DB
try:
    conn=pymongo.MongoClient()
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" %e

db = conn.db_tweets
collection = db.tweets

# Step 1: Find the top 30 retweets
# I use mongodb's aggregate method to reduce the collection
# retweets start with 'RT', so use regex to match
# then group by the retweet to add how many there are
# then return the retweet and count sorted descending order and limit to 30
# lastly output to a new collection
collection.aggregate([{'$match': {'text':{'$regex':'^RT '}}},
                    {'$group': {'_id': {'text': '$text'},'RTs':{'$sum':1}}},
                    {'$project': {'_id':0, 'RT': '$_id.text', 'Total': '$RTs'}},
                    {'$sort': {'Total':-1}},
                    {'$limit':30},
                    {'$out': 'top_30_RT'}])


# Step 2: Find the associated usernames of the top 30 retweets
# I break down the collection into a list of just the retweets
the_RTs = db.top_30_RT.find({'RT':{'$regex': '@'}},{'_id':0,'RT':1})

# this returns a list of dictionaries of just the retweets, not the id or totals
# now I loop through the list of dictionaries, only returning the values, not the keys
RTs = []
for i in the_RTs:
    RTs += i.values()

# Now that we have a python list of just the retweets, 
# we can find the user retweeted
# Retweets start with a reference to the user, the '@' character
# the refernce is concluded with the ':' character
start = '@'
end = ':'

# I loop through the list of retweets and only return the RT usernames
usernames = []
for tweet in RTs:
    user = str(tweet[tweet.find(start)+1:tweet.find(end)])
    usernames.append(str(user))

# create list of distinct usernames
retweeted_usernames = list(set(usernames))

# Step 3: Find the location of the users who retweeted
locations = db.tweets.find({'user.screen_name': {'$in': retweeted_usernames}}, 
    {'_id':0, 'user.screen_name':1, 'user.location':1})

# loop through cursor to return key:value pairs of screen_names and locations
loc = []
for locale in locations:
    loc += locale.values()

