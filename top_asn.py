#!/usr/bin/python3
#2022.12.01: Program Get Top Source IP Address on Specific Port
#2023.01.13: AS毎の送信仕方を抽出する
#            特定のポートに対する、送信パケットが多かったAS順に並び替える。

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

        #Shiraishi moto no co-do
        srcip = socket.inet_ntoa(ip.src)

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
        #Count packet
        if(dport == target_port):
            packet_counter += 1
            if srcip in srcip_list:
                srcip_list[srcip] += 1
            else:
                srcip_list[srcip]  = 1

print("Packet on {} {}: {}".format(target_port, filename, packet_counter))

#####追加した部分####
reader = geoip2.database.Reader('./geo_asn/GeoLite2-ASN.mmdb')
asn_list = {}

for ip in srcip_list:
    try:
        response = reader.asn(ip)
    except:
        asn = -1
        continue
    asn = response.autonomous_system_number
    if asn in asn_list:
        asn_list[asn] += int(srcip_list[ip])
    elif asn not in asn_list:
        asn_list[asn] = int(srcip_list[ip])

top_asn_sorted = sorted(asn_list.items(), key=lambda x:x[1], reverse=True )
fp = open(ofile, "w")
writer = csv.writer(fp)
writer.writerows(top_asn_sorted)
fp.close()

#Out put sorted list to .csv file
#top_src_sorted = sorted(srcip_list.items(), key=lambda x:x[1], reverse=True )
#fp = open(ofile, "w")
#writer = csv.writer(fp)
#writer.writerows(top_src_sorted)
#fp.close()
