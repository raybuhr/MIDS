#Kasane Utsumi 
#tfIdf.py
#This is a utility module calculates td-idf and returns it. 

import math 
import re
import string
import signal

#handle interrupt gracefully
def interrupt(signum, frame):
   print "Interrupted, closing ..."
   exit(1)


class TfIdf:

	lengthOfCorpus = 0
 	numDocWithWords = 0
	keyword = ''

	def __init__(self, lengthOfCorpus=0,numDocWithWords=0,keyword = ''):
      		self.lengthOfCorpus = lengthOfCorpus
      		self.numDocWithWords = numDocWithWords
		self.keyword = keyword

	#This line cleans up body of text, basically following the same steps during map reducing to get number of times words appear in an article.
	#Returns an array which will be used to calculate TF
	def getArrayOfCleanedWords(self,document):
		if document == None:
			return []				
		
		processedArray = []
	
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


		body = document.strip()
		#words = line.split(" ")
		#split up by space, period, and other whitespace characters
		words = re.split('\s|(?<!\d)[,.]|[,.](?!\d)', body)
	
		# add to the array of wrods where 
		for word in words:
			word = word.lower()
			word = word.strip()
			
	        	#remove leading and trailing punctuations
	    		word = re.sub('[%s]' % re.escape(string.punctuation), '', word)
	
			#ignore word that is empty or is a stop words since we didn't count those for during document count for each word
			if ((len(word) == 0) or (word in stops)):
				continue
			processedArray.append(word.encode('utf8'))
		return processedArray
	
	#calculates tf	
	def tf(self,doc):
	    
	    #get an array of all of the words (except for stop words) in the document
	    splittedWords = self.getArrayOfCleanedWords(doc)
	    	
	    #print(len(splittedWords))
	    #print ("obama" + str(splittedWords.count(self.keyword.lower()))) 
	    if (len(splittedWords) == 0): #for some reason the document doesn't contain any import words. Prevent division by 0.  
		return 0
	    return splittedWords.count(self.keyword.lower()) / float(len(splittedWords))
   
	#calculates idf	
	def idf(self):
	    #print float(self.lengthOfCorpus)
    	    #print float(self.numDocWithWords)  
	    return 1.0 + math.log(float(self.lengthOfCorpus) / float(self.numDocWithWords))

    #return 1.0 + math.log(float(len(corpus)) / num_doc_with_term)

   
	#calculates tf-idf	
	def Calculate(self,doc):
    		return self.tf(doc) * self.idf() 



