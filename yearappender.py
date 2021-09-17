## A password dictionary enhancer. The script prepends and appends years and 
## sequence numbers to strings in an input file and writes to a new, more 
## comprehensive dictionary file. 

from sys import argv
# from getopt import getopt

# infile is the list of passwords that should be permutated, provided by the user
with open(argv[1],'r') as infile:
	# IPs = infile.readlines()
	passwords = [line.strip() for line in infile]
infile.close()

# prepend and append numbers
with open(argv[2],'w') as outfile:
	for pword in passwords:
		# start by writing the original string to the output fil
		outfile.write(pword+"\n")
		
		# prepend and append all numbers between 0 and 10000
		for j in range(0,10000):
				outfile.write(pword+str(j)+"\n")
				outfile.write(str(j)+pword+"\n")
		
		#  
		for year in range(2000,2019):
			outfile.write(pword+str(year)+"\n")
			outfile.write(str(year)+pword+"\n")
			for i in range(0,13):
				outfile.write(pword+str(year)+str(i)+"\n")
				outfile.write(str(year)+str(i)+pword+"\n")
outfile.close()
