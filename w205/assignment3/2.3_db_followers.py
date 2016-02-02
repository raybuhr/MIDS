'''
2.3­ Write a python program to create a db called db_followers that stores all the followers
for all the users that you find in task 2.1. Then, write a program to find the un­followed
friends after a week for the top 10 users( users that have the highest number of followers
in task 2.1) since the time that you extracted the tweets.
'''
import pymongo
import tweepy

# Step 1: Store followers from 
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

# Step 1: create a db of the followers of users from task 2.1
old_db = conn.db_tweets
# create collection of all users from 2.1
old_db.tweets.aggregate([{'$match': {'user.screen_name':{'$exists':'true'}}},
<<<<<<< HEAD
						{'$group': {'_id': {'user': '$user.screen_name'},'tweets':{'$sum':1}}},
						{'$project': {'_id':0, 'user': '$_id.user', 'Tweets': '$tweets'}},
						{'$sort': {'Tweets':-1}},
						{'$out': 'users'}])
=======
                        {'$group': {'_id': {'user': '$user.screen_name'},'tweets':{'$sum':1}}},
                        {'$project': {'_id':0, 'user': '$_id.user', 'Tweets': '$tweets'}},
                        {'$sort': {'Tweets':-1}},
                        {'$out': 'users'}])
>>>>>>> 5ba6343218b2c08c3f25266aab278c757a52db6e

# Step 2: find the top 10 users
# query users and return 10 users with followers_count sorted descending
top_10_query = [] 
for doc in db.tweets.find({},{'_id':0,'user.screen_name':1,'user.followers_count':1}).sort('user.followers_count', pymongo.DESCENDING)[0:10]:
    top_10_query += doc.values()

# parse through the dict output from the query to return just the username with followers count
top_10_pair = []
for pair in top_10_query:
    top_10_pair += pair.values()
# split the list of user and follower counts to get the top 10 users
top_10_users = []
top_10_users = top_10_pair[1::2]


# Step 3: store followers of the top 10 users
# create db_followers
followers = conn.db_followers.followers

# Use Tweepy to collect the followers for the top 10 users
# Twitter authorization
consumer_key = "g7WaeKhJUdXERWi7TBG2ET1hc";
consumer_secret = "cfNMs6S91KcIJuuQkWmAMem8ogY99F1ZbZr83fMCkJupxNstdh";
access_token = "63479910-PPtHT52R6zjhaQFiGYJPSfYwOCnDUyxn9LGI7ffEI";
access_token_secret = "FkUmm1mhuIvoKMfEtlPG1bYqIBCQ3k4Cephf1cJCWta6K";

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


# use Tweepy search api to return followers and insert to db_followers.followers
for users in top_10_users:
    for user in tweepy.Cursor(api.followers, screen_name=users.encode('utf8')).items():
        data = {}
        data[str(users)] = str(user.screen_name) 
        followers.insert(data)

# Step 4: Find the un-followed users
# To find the un-followed, need to create another collection to compare to the previous
# run the tweepy search for followers and store to followers2
followers2 = conn.db_followers.followers2
# Then we need to add followers after one week
'''
In case you want to run the program in the background for over a week...
import time
time.sleep(604800) # sleep for one week
'''
for users in top_10_users:
    for user in tweepy.Cursor(api.followers, screen_name=users.encode('utf8')).items():
        data = {}
        data[str(users)] = str(user.screen_name)
        followers2.insert(data)

# Compare unfollowed to followers
# Logic:
# if user in followers not in unfollowed, then user unfollowed
# else user is still following
unfollowed = []
follow1 = []
follow2 = []
# add screen name of followers in week1 to list
for doc in followers.find({},{'_id':0,'follower':1}):
    follow1 += doc.values()
# add screen name of followers in week2 to list
for doc in followers2.find({},{'_id':0,'follower':1}):
    follow2 += doc.values()
# compare each person in week1 list to week2 list
# if person is not in week2, add to unfollowed list
for person in follow1:
<<<<<<< HEAD
	if person not in follow2:
		unfollowed.append(str(person))
# add people that unfollowed to a MongoDB collection
unfollowers = conn.db_followers.unfollowed
for person in unfollowed:
	data = {}
	data['unfollower'] = str(person)
	unfollowers.insert(data)
=======
    if person not in follow2:
        unfollowed.append(str(person))
# add people that unfollowed to a MongoDB collection
unfollowers = conn.db_followers.unfollowed
for person in unfollowed:
    data = {}
    data['unfollower'] = str(person)
    unfollowers.insert(data)
>>>>>>> 5ba6343218b2c08c3f25266aab278c757a52db6e
