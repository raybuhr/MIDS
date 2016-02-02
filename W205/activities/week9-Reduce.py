import sys

def wcount(prev_key, counts):
	if prev_key is not None:
		print prev_key + " count is " + str(counts)

prev_key = None
counts = 0
for line in sys.stdin:
	key, value = line.split("\t",1)
	if key!=prev_key:
        wcount(prev_key, counts)
        prev_key = key
        counts = 0
    counts += eval(value)

wcount(prev_key, counts)
