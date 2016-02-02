import sys

w_counts = {}

for line in sys.stdin:
	words = line.split()
	for word in words:
		w_counts[word] = w_counts.get(word, 0) + 1

print w_counts
