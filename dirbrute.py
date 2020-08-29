#!/usr/bin/python

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import string
import sys

host=str(sys.argv[1])
#host="http://www.sec542.org/"
print("Guessing directories on: " + host + "...")

for c1 in string.ascii_lowercase:
    for c2 in string.ascii_lowercase:
        for c3 in string.ascii_lowercase:
            directory = c1+c2+c3
            response = requests.get((host + directory) ,verify=False)
            if response.status_code < 400:
                print(host + directory + " : " + str(response.status_code))


