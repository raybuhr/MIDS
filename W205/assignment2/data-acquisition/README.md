#Acquisition Task#

Acquire relevant data around the Microsoft / Mojang for a recent week. To accomplish this, do the following:

- Write an acquisition program that can acquire tweets for a specific date on the using the Tweepy python package. The program should pull tweets for the #microsoft and #mojang hash tags simultaneously.
	- see twitter-parse.py

- Run your data analysis over a week period of time. You should chunk your data as appropriate and give yourself the ability to re-run the process reliable in case of failures.
	- see json-parse.py

- Organize the resulting raw data into a set of tweets and store these tweets into S3.
	- http://s3-us-west-2.amazonaws.com/rbuhr-tweets

- Analyze the tweets by producing a histogram (a graph) of the words.
	- see histogram_all_tweets.png for graph of all word frequency
	- see histogram_top50.png for graph of the 50 most common words

