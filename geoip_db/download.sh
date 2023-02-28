# !/usr/bin/bash

curl "https://download.maxmind.com/app/geoip_download_by_token?edition_id=GeoLite2-ASN&date=20230113&suffix=tar.gz&token=v2.local.Wjvgs1vhO1XcDnzDe1tpGgUk0ktb3pTygjNI2XuzmheB7eLSL15Bn6cb6G9fkIJdDeZR0VILVcMKpRAxbE8CyonRU-ch6wZZTkBDOPfmbQAfsoPGwJnZvp0kl2ZedlUyP-HPgIyI2lYHp6Ow4TZ5t7r3iX6RDILEUhrYVWPCIeKqbLvaxrnGfaF_tAn3JO1I3JOU2Q" -o GeoIP_ASN.gz

tar -xf GeoIP_ASN.tar.gz
