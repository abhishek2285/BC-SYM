#!/bin/sh

high="speedtest/random1000x1000.jpg"
file="index.html"
#echo "High traffic(high) or Low traffic(low)"
#read traffic
#echo $traffic

echo Number of Tun = $1

traffic="high"

if [ $traffic == high ]
then
	file=$high
fi

numTun=$1
counter=0
TunIP=2
while [ $counter -lt $numTun ]; do
	wget http://200.0.0.$TunIP/mini/$file
	let counter=counter+1 
	let TunIP=TunIP+1 
done

echo DONE

if [ $traffic == high ]
then
	numFiles=$( ls | grep random1000 | wc -l )
else
	numFiles=$( ls | grep index.html | wc -l )
fi

echo Number of File=$numFiles
if [ $numFiles == $numTun ]
then
	echo "PASS: Traffic PASS on all tunnels"
else
	echo "FAIL: Traffic pass on $numFiles"
fi

rm -f index.html*
rm -f random1000*
