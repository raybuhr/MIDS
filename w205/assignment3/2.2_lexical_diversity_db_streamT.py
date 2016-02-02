'''
2.2­ Compute the lexical diversity of the tweets stored in db_streamT and store the results
back to Mongodb. You need to create a collection with appropriate structure for storing the
results of your analysis.
'''

import nltk
import pymongo

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

db = conn.db_streamT
collection = db.tweets

# Lexical divsersity is the amount of distinct words in a corpus divided by
# the total number of words in that corpus

# The corpus of the tweets in db_streamT will be just the tweets
# Query db_streamT for just the text of the tweets
tweet_corpus = collection.find({},{'_id':0,'text':1})

# Store results of query to a list
corpus = []
for tweet in tweet_corpus:
    corpus += tweet.values()
# Join that list to a single volume of text
corpus_text = ''
corpus_text = corpus_text.join(corpus)

# The words in the corpus need to be extracted
corpus_words = corpus_text.split()
# Then we need isolate just the distinct words
corpus_words = set(corpus_words)

# Compute the Lexical Diversity of tweets
num_words = float(len(corpus_words))
words_in_text = float(len(corpus_text))

print "The lexical divsersity of the tweets in db_streamT is:"
print num_words / words_in_text

# Store the results back to MongoDB
# store the corpus as a collection of a single key:value pair
db.corpus.insert('text': corpus_text)
# store the distinct words as a series of key:value pairs
word_store = {}
word_counter = 1
for word in corpus_words:
    word_store.update({str(word_counter):word})
    word_counter += 1
db.words.insert(word_store)

