# My collection of personal pentest tools
Some scripts written to learn python, others to be more efficient during pentesting. Put on github to learn git and github.

## p-permuter.py
Prepends and appends numbers and special characters to words in an input file and writes to an output file. Useful for password spraying and/or customized cracking.

## kerbspray.sh
A wrapper around the fantastic https://github.com/ropnop/kerbrute. It adds the capability to use a file with passwords to spray, as well as limit and delay parameters to avoid hitting the account lockout threshold in Windows domains. 

## ftplister.py
Takes a list of IP addresses, logs in to FTP anonymously and lists contents of FTP landing folder of each host.box

## bauthbrute.py
Takes a host, username and a password file and brute force guesses password + a two character password suffix for that user.

## dirbrute.py
Brute force guesses all three-character directories on a host. E.g. from example.com/aaa to example.com/zzz.

## headers.py
Takes a list of hosts, makes a GET to the web root and lists "Server" response headers.

## endpointSweep.py
Takes a file of `METHOD /path` lines and sweeps them against a base URL, displaying results in a color-coded table (green=2xx, red=4xx/5xx). Supports API key and Bearer token auth via environment variables, routes through Burp proxy by default (use `--no-proxy` to bypass), and allows filtering by HTTP method. Response bodies are truncated with an ellipsis indicator; truncation length is configurable with `--body-length`.
