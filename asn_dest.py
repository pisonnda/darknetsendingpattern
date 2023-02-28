#!/usr/bin/python3
#2022.12.01: Program Get Top Source IP Address on Specific Port
#2023.01.13: Convernt to: Time,AS,Destination

import csv
import dpkt
import geoip2.database
import socket
import sys

#Syntax Check
if len(sys.argv) < 3: 
    print("Syntax Error")
    print("Syntax: top_src.py <port> <pcap_file.pcap> <output_file.csv>")
    sys.exit()
# Read Data Base of ASN
reader = geoip2.database.Reader('./geo_asn/GeoLite2-ASN.mmdb')

# Data
data = []

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
        #IP Filtering
        isrcip = int.from_bytes(ip.src, "big")
        dstip = int.from_bytes(ip.dst, "big")
        #送信元を無視する
        if (isrcip & 0xFFFFF000) == 0xCA195000: continue
        #SINET
        if  isrcip == 0x9663C7E1 or \
            isrcip == 0x9663C7E2 or \
            dstip == 0x9663C7E2:
                continue
        #HONEYPORT
        if dstip == 0xCA19550A or \
        dstip == 0xCA195510:
            continue

        #Get destination port
        if ip.p == dpkt.ip.IP_PROTO_TCP:
            TCP = ip.data
            try: 
                dest_port = TCP.dport
            except:
                continue
        elif ip.p == dpkt.ip.IP_PROTO_UDP: 
            UDP = ip.data 
            try: 
                dest_port = TCP.dport
            except:
                continue
        else: continue

        dport = int(dest_port)
        if(dport == target_port):
            #Shiraishi moto no co-do
            src_ip = socket.inet_ntoa(ip.src)
            dest_ip = socket.inet_ntoa(ip.dst)
            try:
                response = reader.asn(src_ip)
            except:
                asn = -1
                continue
            asn = response.autonomous_system_number
            data.append("{},{},{}".format(ts, asn, dstip))

with open(ofile, "w") as fp:
    fp.write('\n'.join(data))
fp.close()
