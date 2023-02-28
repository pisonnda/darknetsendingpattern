awk -F, '{if($2==7713){print $0}' 445_port.csv > AS7713.csv
