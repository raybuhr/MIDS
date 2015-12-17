#Words with the Media:
##Predicting News You Will Enjoy

MIDS W205: Storing and Retrieving Data
Kasane Utsumi, Katie Adams, Raymond Buhr, Julian Phillips


Fifty years ago, there were far fewer sources of news than there are today. Then, your media was one of three television stations (only at certain hours of the day), the daily newspaper and radio programs. Today, aside from the numerous dedicated television channels at your disposal for 24 hour news coverage, there are tens of thousands of news websites and blogs with different perspectives.

Various news media has discovered that portraying the news in the manner that the viewer/reader desires can lead to an increase in revenue as more is accessed. With that in mind:

####*Is it possible to predict a different news source that a person would enjoy based on how a known news source treats a topic?*



###Data Acquisition
- Twitter - See TweetAcquisitionAndUpload.py
- New York Times - See nytimes.py
- Daily Beast - See DailyBeast_scraper.py
- CNN Transcipts - See CNN_scraper.py
- Various News Sites* = See newspaper_aggregator.py
  *we used the *newspaper* library for python which has a list of ovor 200 popular news sites
  
###Data Storage
- We stored all of our scraped news articles into DynamoDB hosted by AWS.
- We used *boto* for python to create and update the tables.

###Data Manipulation and Processing
- Extracting articles stored in the "newspaper" table into their own table by source - see 
- Adding polarity, subjectivity and lexical diversity to each source table - See addtextblobattrs.py
- Calculating TF-IDF - see mapperDailyBeast.py for the mapper portion of MapReduce and reducer.py for the reducer portion, then check out both streamingHQL and interactiveHQL two different ways to use AWS EMR to calculate TF-IDF
- Calculating percentage of common English words - see top1000.py for the list of 1,000 most common words, then add_text_stats.py for code to update the tables

- Within the Data_Maniupulation_TF_IDF Folder:
- DocumentCountForEachWord” folder contains scripts used to count in how many documents each word appears. 
- mapperDocCount.py – python file called by hql files above for mapping. For each document fed into the mapper, it outputs a word and “1” if a word appears in the document. Stop words are excluded. 
- reducerDocCount.py  -- python file called by hql files above for reducing. It will add up all of the lines per each word and output a word and number of documents the word appears in. 
- fillTDIDFValues.py -  fills “TfIdfNew” table with Tf-Idf value for a given keyword (passed as argv) for each articles in a given source. For example, if keyword "obama" is passed, and DailyBeast is specified as a source, it calculate Tf-Idf for every article in DailyBeast table that contains a word "obama" and adds row to the  "TfIdfNew" table
- tfIdf.py - a utility module which calculates tf-idf and returns it. 

- Within the Word Association Count Folder:
- Python and Hql files used for two map reduce jobs
- Word count of all words in new York times corpus 1)	mapperWordCount.py – Python mapper for simple word count
2)	reducer.py – Python reducer 3)	nyt_word_count.hql – Hql code that runs map reduce job using mapper and reducer above, and dumps result into a file on S3
- For 100 most frequent words from the word count above, we found out what words were associated with them the most. 
1)	Mapperkeyword.py – Python mapper which contains an array of 100 most frequent words (from EMR job above), and for each word that appears in the same doc outputs both words put together with a delimiter.2)	Reducerkeyword.py – Python reducer
3)	Nyt_word_keyword.hql – Hql code that runs map reduce job using mapper and reducer above, and dumps result into a file on S3





###Data Output and Interactivity
- Comparing word usage - see CompareSources.py
- Flask app for end user interactivity - see flaskapp.py
- Within the Interactivity Folder (A mixture of files used for interactive web application):
- Index.py is Flask-driven web application used for interactive demo.  It supports two flows:
1) Recommend a news source based on a keyword and current news source a user reads
2) Based on the keyword entered, it will output average subjectivity, polarity, lexical diversity and article count of all articles (in which keyword id relevant enough per Tf-Idf value) from each source in a bar chart format. Bar chart was created using D3



###Future Vision
We were able to create a prototype on small scale that proved that the idea was feasible. However, there are many other features and capabilities that we feel that a full version of this application could have. Some of them that we envision include:
- The ability for the end user to adjust the TF-IDF output for the keyword on a sliding scale. This would allow them to set the threshold either higher or lower than default when determining that a given article covered their term. 
- Changes in how articles are compared to each other. Today only lexical diversity, polarity and subjectivity are used to determine if sources are alike. There are many other metrics that can be used though such as reading level, percent of common words used and others. Additionally, the consumer should be able to change the weightings of each measure to what suits them best could be added.
- The system architecture could be drastically improved. Adding all of the attributes at the same time rather than multiple scans would be ideal. As discussed in the DynamoDB section, changes to the hash and range key and standardization of the dates would be fixed as well.
- The speed of returning matches is not optimized and would have to be considered in any final project. Putting all items into the database in a consistent format would improve this part of the project along with allowing for more throughput within DynamoDB.
- Perhaps a final vision would be making the end product similar to what Pandora does for music. The end user can create a starting point and then rate each new newsource and the application can learn what they enjoy to read and will present them with those findings regardless of the initial search term.


