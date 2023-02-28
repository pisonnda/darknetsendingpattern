#!/usr/bin/bash
#$1: Pcapfile (pcap_file)
#$2: Top n Source IP (num)
pcap_file=$1
num=$2

#Get Top_port from pcap file
#Syntax: top_port.py <pcap_file1> <pcap_file2>
echo "Get top_port"
python3 top_port.py $pcap_file
top_port_ofile=`basename $pcap .pcap`_top_port.csv

#Get Top_Srcip with top 5 port
#Syntax: top_src.py <port> <pcap_file.pcap> <output_file.csv>
echo "Get top_srcip"
head $top_port_ofile -n 5 | cut -d ',' -f1 | while read port;
do
    python3 top_src.py $port $pcap_file $port.csv
done

#Convert IP address to Country
echo "Convert ip to country code"
./convert_ip_2_country.sh $port.csv $num
