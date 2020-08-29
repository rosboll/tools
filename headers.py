#!/usr/bin/python

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#read hosts
with open('hostnames.txt') as f:
    hosts=f.read().splitlines()

#for each host
for host in hosts:
    response = requests.get(host,verify=False)
    print(host + ': ' + response.headers['server'])

