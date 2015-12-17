import string
import sys
from top1000 import top1000
import boto.dynamodb

# Step 1: Connect to DynamoDB
conn = boto.dynamodb.connect_to_region(
       'us-west-2',
       aws_access_key_id='key',
       aws_secret_access_key='secret')

# Step 2: Connect to table given via command line 
table = conn.get_table(sys.argv[0])
scan = table.scan()
data = list(scan)

# Step 3: Iterate through each item in table and add linguistic metrics
for item in data:
    try:
        # first remove punctuation from article text
        text_wo_punc = item['body'].encode('utf-8').translate(None, string.punctuation)
        # then create a list of the words used in the article
        text_words = text_wo_punc.split()
        # measure the number of characters without spaces
        text_length = len(text_wo_punc) - len(text_words) - 1 #to discount spaces
        # calculate average word length as number of chars over number of words
        text_avg_word_length = float(text_length) / len(text_words)
        # measure the percent of text that is punctuation
        percent_punc = 1 - float(len(text_wo_punc))/len(item['body'])
        # count the number of words used among the 1000 most common English words
        in_top1000 = 0
        for word in text_words:
            if word in top1000:
                in_top1000 += 1
        # add these metrics back to the DynamoDB table
        line['avg_word_length'] = text_avg_word_length
        line['percent_punctuation'] = percent_punc
        item['percent_top1000'] = float(in_top1000)/len(text_words)
        item.put()
        item.save()
    except:
        continue
