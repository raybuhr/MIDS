#! /usr/bin/python
# -*- coding: utf-8 -*-

from urllib import urlopen
from bs4 import BeautifulSoup
import re

# Copy all of the content from the provided web page
webpage = urlopen(‘http://www.huffingtonpost.com/search.php/?q=Search+The+Huffington+Post&s_it=header_form_v1’).read()

'''

# Grab everything that lies between the title tags using a REGEX
patFinderTitle = re.compile(‘<title>(.*)</title>’)

# Grab the link to the original article using a REGEX
patFinderLink = re.compile(‘<link rel.*href=”(.*)” />’)

# Store all of the titles and links found in 2 lists
findPatTitle = re.findall(patFinderTitle,webpage)
findPatLink = re.findall(patFinderLink,webpage)

# Create an iterator that will cycle through the first 16 articles and skip a few
listIterator = []
listIterator[:] = range(2,16)

# Print out the results to screen
for i in listIterator:
print findPatTitle[i] # The title
print findPatLink[i] # The link to the original article

articlePage = urlopen(findPatLink[i]).read() # Grab all of the content from original article

divBegin = articlePage.find(‘<div>’) # Locate the div provided
article = articlePage[divBegin:] # Copy the characters after the div

# Pass the article to the Beautiful Soup Module
soup = BeautifulSoup(article)

# Tell Beautiful Soup to locate all of the p tags and store them in a list
paragList = soup.find_all(‘p’)

# Print all of the paragraphs to screen
for i in paragList:
print i

print “\n”

'''

# Here I retrieve and print to screen the titles and links with just Beautiful Soup
soup2 = BeautifulSoup(webpage)

print soup2.find_all(‘title’)
print soup2.find_all(‘link’)

titleSoup = soup2.find_all(‘title’)
linkSoup = soup2.find_all(‘link’)

for i in listIterator:
print titleSoup[i]

print linkSoup[i]
print “\n”
