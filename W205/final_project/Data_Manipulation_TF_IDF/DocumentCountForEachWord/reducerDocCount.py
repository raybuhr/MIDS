#!/usr/bin/python
#Kasane Utsumi - 05/02/2015
#reducerDocCount.py
#reducer used during mapreduce job to count how many document contains each word

import sys   

def wcount(prev_key,counts):
   if (prev_key is not None and len(prev_key) != 0 and counts is not None):
 	print '%s\t%s'% ( prev_key, str(counts))
     

prev_key = None
counts = 0

for line in sys.stdin:
   line = line.strip()

   key,value = line.split("\t",1)
   
   try:
        value = int(value)
   except ValueError:
        continue

   #by the time this is run, the list would be sorted by a word. We just need to keep adding until we run into a different word.
   if key != prev_key:
      wcount(prev_key,counts)
      prev_key = key
      counts = 0
   counts +=value

wcount(prev_key,counts)


