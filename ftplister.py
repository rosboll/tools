#!/usr/bin/python

from ftplib import FTP
from sys import argv
# from getopt import getopt

# Read IP addresses from file
with open(argv[1],'r') as infile:
	# IPs = infile.readlines()
	IPs = [line.strip() for line in infile]
infile.close()

# print(IPs)

# Log in anonymously and list contents of FTP landing folder on each IP 
for ip in IPs:
	ftp = FTP(ip)
	# ftp.set_debuglevel(1)
	ftp.login()
	print("Contents in %s:") % (ip)
	ftp.retrlines('LIST')
	ftp.quit()
