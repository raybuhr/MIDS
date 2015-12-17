#!/usr/bin/python
#Kasane Utsumi - 05/02/2015
#mapperDotCount.py
#Mapper used during mapreduce job to count how many document contains each word

import sys
import string
import re

#I did not use nltk's stop words because EMR was crushing while importing stopwords even though nltk installation was ran during bootstrapping.
#from nltk.corpus import stopwords

#stops = set(stopwords.words('english'))
#Since I could not use nltk's stop words, I hard coded stop words. 
stops = ['i', 'me', 'my', 'myself', 'we',
      'our', 'ours', 'ourselves', 'you', 'your', 'yours',
      'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
      'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
      'they', 'them', 'their', 'theirs', 'themselves', 'what',
      'which', 'who', 'whom', 'this', 'that', 'these', 'those',
      'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
      'have', 'has', 'had', 'having', 'do', 'does', 'did',
      'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
      'because', 'as', 'until', 'while', 'of', 'at', 'by',
      'for', 'with', 'about', 'against', 'between', 'into',
      'through', 'during', 'before', 'after', 'above', 'below',
      'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
      'over', 'under', 'again', 'further', 'then', 'once',
      'here', 'there', 'when', 'where', 'why', 'how', 'all',
      'any', 'both', 'each', 'few', 'more', 'most', 'other',
      'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
      'so', 'than', 'too', 'very', 's', 't', 'can', 'will',
      'just', 'don', 'should', 'now']

regex = re.compile('[%s]' % re.escape(string.punctuation))


for line in sys.stdin:

	found = set([])

	line  = line.strip()
	#words = line.split(" ")
	words = re.split('\s|(?<!\d)[,.]|[,.](?!\d)', line)

	# write the tuples to stdout
	for word in words:
		word = word.lower()
		word = word.strip()

		#removing any leading and trailing punctuations.		
    		word = re.sub('[%s]' % re.escape(string.punctuation), '', word)

		#1. if word is empty after stripping out spaces and punctuations, ignore. 
		#2. if word is is a stop word, ignore.
		#3. if word is already counted in this document, ignore 
		if ((len(word) == 0) or (word in stops) or word in found):
			continue
		#add word to "found" set so it won't be counted again within a same document
		found.add(word)
		
		print '%s\t%s' % (word, "1")
