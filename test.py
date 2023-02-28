#!/usr/bin/python3
# 2022.01.13    Version1: Convert IP -> AS Number (Pison)
#               python3 test.py <IP_Address>
# Databaseの使い方: https://takahoyo.hatenablog.com/entry/2015/01/20/115031 (Japanese)
#                   https://github.com/maxmind/GeoIP2-python (FULL)


import geoip2.database

reader = geoip2.database.Reader('./geo_asn/GeoLite2-ASN.mmdb')
ip_addr = '202.25.82.64'
record = reader.asn(ip_addr)
asn = record.autonomous_system_number
org = record.autonomous_system_organization

print("{},{},{}".format(ip_addr, asn, org))



#------------------How to use Database---------------#
# GET AS Number
#   with geoip2.database.Reader('/path/to/GeoLite2-ASN.mmdb') as reader:
#       response = reader.asn('203.0.113.0')
#       response.autonomous_system_number
# -> 1221
#       response.autonomous_system_organization
# -> 'Telstra Pty Ltd'
#       response.ip_address
# -> '203.0.113.0'
#       response.network
# -> IPv4Network('203.0.113.0/24')

# Get Domain 
#       response = reader.domain('203.0.113.0')
#       response.domain
# -> 'umn.edu'
#       response.ip_address
# -> '203.0.113.0'

# Get IPS Infor
#   with geoip2.database.Reader('/path/to/GeoIP2-ISP.mmdb') as reader:
#       response = reader.isp('203.0.113.0')
#       response.autonomous_system_number
# -> 1221
#       response.autonomous_system_organization
# -> 'Telstra Pty Ltd'
#       response.isp
# -> 'Telstra Internet'
#       response.organization
# -> 'Telstra Internet'
