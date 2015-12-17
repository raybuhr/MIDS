#!/usr/bin/python
#Kasane Utsumji
#reducerKeyword.py
#Python reducer, adds up count of all words

#!/usr/bin/python
import sys

# maps words to their counts
word2count = {}

for line in sys.stdin:
    line = line.strip()

    # parse the input we got from mapper.py
    word, count = line.split('\t', 1)
    # convert count (currently a string) to int
    try:
        count = int(count)
    except ValueError:
        continue

    try:
        word2count[word] = word2count[word]+count
    except:
        word2count[word] = count

# write the tuples to stdout
# Note: they are unsorted
for word in word2count.keys():
    print '%s\t%s'% ( word, word2count[word] )
