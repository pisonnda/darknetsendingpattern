# Step 1: Get Top AS Number
# python top_asn.py <port> <pcap_file> <out_file.csv>
python top_asn.py 445 ../../pcap/20200210200001.pcap 445_asn.csv

# Step 2:Get [Timestamp - AS - NDA's Destination IP] infor (All Packets)
# python asn_dest.py <port> <pcap_file> <output-file.csv>
python asn_dest.py 445 ../../pcap/20200210200001.pcap 445_port.csv

# Step 3: Get Packets info of particular AS (Ex: AS45899)
awk -F, '{if($2==45899){print $0}}' 445_port.csv > AS45899.csv

# Step 4: Make Graph
#gnuplot -c plot.p <output.png> <Title> <Input.csv>
gnuplot -c plot.p as45899.png AS45899 AS45899.csv

