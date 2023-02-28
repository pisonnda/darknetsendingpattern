#!/usr/bin/python3
#2022.12.01: Program Get Top Source IP Address on Specific Port
import csv
import dpkt
import socket
import sys

#Syntax Check
if len(sys.argv) < 3: 
    print("Syntax Error")
    print("Syntax: top_src.py <port> <pcap_file.pcap> <output_file.csv>")
    sys.exit()

#Get port - filename - ofile
target_port = int(sys.argv[1])
filename = sys.argv[2]
ofile = sys.argv[3]

#Definition
packet_counter = 0
srcip_list = {}
pcr = dpkt.pcap.Reader(open(filename,'rb'))

#Read Pacapfile and Count packet of each Source IP
for ts,buf in pcr:
    try:
        eth = dpkt.ethernet.Ethernet(buf)
    except:
        print('Fail parse FrameNo:', packet_count, '. skipped.')
        continue
    if type(eth.data) == dpkt.ip.IP:
        ip = eth.data
        srcip = socket.inet_ntoa(ip.src)
        #Get destination port
        if ip.p == dpkt.ip.IP_PROTO_TCP:
            TCP = ip.data
            dport = TCP.dport
        elif ip.p == dpkt.ip.IP_PROTO_UDP:
            UDP = ip.data
            dport = UDP.dport
        #Count packet
        if(int(dport) == target_port):
            packet_counter += 1
            if srcip in srcip_list:
                srcip_list[srcip] += 1
            else:
                srcip_list[srcip]  = 1

print("Packet on {} {}: {}".format(target_port, filename, packet_counter))
#Out put sorted list to .csv file
top_src_sorted = sorted(srcip_list.items(), key=lambda x:x[1], reverse=True )
fp = open(ofile, "w")
writer = csv.writer(fp)
writer.writerows(top_src_sorted)
fp.close()
print("------------------------")
