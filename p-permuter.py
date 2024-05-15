## A password dictionary enhancer. The script prepends and appends years and 
## sequence numbers to strings in an input file and writes to a new, more 
## comprehensive dictionary file. 

# Variables
startIterator   = 0
stopIterator    = 25
fromYear        = 2020
toYear          = 2024
specials        = ['!','.','-','_','@',]

from sys import argv
# from getopt import getopt

# infile is the list of passwords that should be expanded, provided by the user
with open(argv[1],'r') as infile:
    # IPs = infile.readlines()
    passwords = [line.strip() for line in infile]
    infile.close()

# prepend and append numbers
with open(argv[2],'w') as outfile:
    for pword in passwords:
        # start by writing the original string to the output fil
        outfile.write(pword+"\n")
        
        # prepend and append all numbers from startIterator to stopIterator. Also add special characters from the specials array. 
        for j in range(startIterator,stopIterator+1):
            outfile.write(pword + str(j) + "\n")
            outfile.write(str(j) + pword + "\n")
            for s in specials:
                outfile.write(pword + str(j) + s + "\n")
                outfile.write(pword + s + str(j) + "\n")
                outfile.write(str(j) + s + pword + "\n")
                outfile.write(s + str(j) + pword + "\n")
        
        # prepend and append all years from fromYear to toYear. Also add special characters from the specials array. 
        for year in range(fromYear,toYear+1):
            outfile.write(pword + str(year) + "\n")
            outfile.write(str(year) + pword + "\n")
            for s in specials:
                outfile.write(pword + str(year) + s + "\n")
                outfile.write(str(year) + s + pword + "\n")
                outfile.write(pword + s + str(year) + "\n")
                outfile.write(s + str(year) + pword + "\n")


    outfile.close()
