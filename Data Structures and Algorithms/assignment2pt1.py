'''
Write a scramble function that implements this algorithm. 
For example, the scramble("12") should compute the scramble of "1", which is "1", 
interleaved with the scramble of "2", which is "2". The result is simply "12".

The scramble of “1234” is the interleave of the scramble of “12”, which is “12”, 
and the scramble of “34”, which is similarly “34”. The result is “1324”.

The scramble of “12345678” can be similarly computed as “15372648".

For each of the following messages, add spaces to the end until its length is a power of 2. 
Then compute the scramble of the message.

Message #1: 
'''
msg1 = "Madam I'm Adam."

def next_pwr_of_2(n):
    # returns the next power of 2 >= n.
	return 2**(n-1).bit_length()

