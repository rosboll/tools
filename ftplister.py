#!/usr/bin/python

from ftplib import FTP
from sys import argv
# from getopt import getopt


with open(argv[1],'r') as infile:
	# IPs = infile.readlines()
	IPs = [line.strip() for line in infile]
infile.close()

# print(IPs)


for ip in IPs:
	ftp = FTP(ip)
	# ftp.set_debuglevel(1)
	ftp.login()
	print("Contents in %s:") % (ip)
	ftp.retrlines('LIST')
	ftp.quit()
