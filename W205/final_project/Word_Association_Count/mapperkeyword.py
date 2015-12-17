#!/usr/bin/python
#Kasane Utsumji
#Mapperkeyword.py
#Python mapper which contains an array of 100 most frequent words, and for each word that appears in the same doc outputs both words concatenated with a delimiter inbetween

import sys
import string
import re
#from nltk.corpus import stopwords

#stops = set(stopwords.words('english'))
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

#These were the nouns that was in top 100 in New York Times articles
top_string = 'new	us	two	tuesday	wednesday	thursday	president	friday	monday	years	one	first	york	police	people	world	year	city	government	last	former	would	united	group	three	week	minister	reports	could	home	officials	died	man	million	court	may	federal	time	killed	company	european	day	next	cup	family	top	national	country	obama	military	prime	four	ukraine	house	night	death	made	percent	chief	official	central	help	cut	team	month	wife	many	oil	months	win	reported	news	late	market	five	deal	foundpublic	part	open	china	make	take	days	league	health	life	victory	john	end	north	economy	major	executive	least	children	countrys	war	like	long
'

topWordsArray = top_string.split('\t')


line = sys.stdin.read()
line = line.strip()
line = line.replace('\n', ' ')
words = line.split(" ")




#this will hold array of item with no duplicate, also without "empty" words and no stop words either. 
wordsArray = []	

# write the tuples to stdout
for word in words:
	
	#lowercase the word, strip and whitespace before and after, and remove punctuation from before/after
	word = word.lower()
	word = word.strip();
	word = re.sub('[%s]' % re.escape(string.punctuation), '', word)
	#print word
        #word = regex.sub('',word)

	if ((len(word) == 0) or (word in stops)):
	#if ((len(word) == 0)):
		continue
	
	#we should get only unique words. We don't care if "Obama" occurs x times with "said", but we are more interested in if "Obama" occurred with "said" at all
	if word not in wordsArray:
		wordsArray.append(word)

#print ",".join(wordsArray)
myindex = 0

for topWord in topWordsArray:
	if topWord in wordsArray:
		for word in wordsArray:
			if word != topWord:
 				wordAggr = topWord + 'kasane_Delimiter' + str(myindex) +  'kasane_Delimiter' + word + 'kasane_Delimiter' 
				print '%s\t%s' % (wordAggr, "1")
	myindex += 1

