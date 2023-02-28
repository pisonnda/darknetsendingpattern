#!/bin/bash
#$1: top_src.csv (ソートされた送信元アドレスごとのパケット数）
#$2: top n 行

head $1 -n 5 | while read line
do 
	ip=`echo $line | cut -d "," -f1`;
	n=`echo $line | cut -d "," -f2 | sed 's/\r//'`;
	inf=`geoiplookup $ip`;
	loc=`echo $inf | cut -d ":" -f2;`
	echo -e "$n\t$ip\t->$loc"
done

#---------Old bash script
#python3 fixed_port1.py > test_port53.csv
#cut test_port53.csv -d ',' -f1 | while read ip; 
#do 
#	geoiplookup  $ip
#done
