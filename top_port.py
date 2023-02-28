#!/usr/bin/python3
#2022.12.01: This Program Get Top_Port

import csv
import dpkt
import socket
import sys

#Syntax Check
if len(sys.argv) < 2:
    print("Syntax Error")
    print("Syntax: top_port.py <pcap_file1> <pcap_file2>")
files = sys.argv[1:]

#Main loop
for filename in files:
    ofile = filename[:14] + "_top_port.csv"
    packet_count = 0
    dport_list={}
    print("Handling with file:" + filename)
    pcr = dpkt.pcap.Reader(open(filename,'rb'))
    for ts,buf in pcr:
        packet_count += 1
        try:
            eth = dpkt.ethernet.Ethernet(buf)
        except:
            print('Fail parse FrameNo:', packet_count, '. skipped.')
            continue
        #Get destination port
        if type(eth.data) == dpkt.ip.IP:
            ip = eth.data
            if ip.p == dpkt.ip.IP_PROTO_TCP:
                TCP = ip.data
                dport = TCP.dport
            elif ip.p == dpkt.ip.IP_PROTO_UDP:
                UDP = ip.data
                dport = UDP.dport

            #Count Packet
            if dport in dport_list:
                dport_list[dport] += 1
            else:
                dport_list[dport] = 1

    print("Packet on file {}: {}".format(filename, packet_count))
    #Out put sorted list to .csv file
    top_port_sorted = sorted(dport_list.items(), key=lambda x:x[1], reverse=True )
    fp = open(ofile, "w")
    writer = csv.writer(fp)
    writer.writerows(top_port_sorted)
    fp.close()
    print("------------------------")
