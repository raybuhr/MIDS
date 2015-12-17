#Kasane Utsumi 
#mapperWordCount.py
#Mapper used to count occurrences of all words in a corpus.  
#!/usr/bin/python
import sys
import string
import re
from nltk.corpus import stopwords

stops = set(stopwords.words('english'))
regex = re.compile('[%s]' % re.escape(string.punctuation))

for line in sys.stdin:
	line = line.strip()
	words = line.split(" ")
	# write the tuples to stdout
	for word in words:
		word = word.lower()
		word = word.strip();

	        #remove punctuation
		word = re.sub('[%s]' % re.escape(string.punctuation), '', word)
        	#word = regex.sub('',word)


		#if word is empty after stripping everything out, or if word is stop word just ignore
		if ((len(word) == 0) or (word in stops)):
			continue

		print '%s\t%s' % (word, "1")
