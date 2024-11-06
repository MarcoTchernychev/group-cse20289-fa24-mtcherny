#sbs.sh
#Alicia Melotik
#amelotik.nd.edu
#Marco Tchernychev
#mtcherny@nd.edu

#!/bin/bash
#set -x

#check for proper number of arguments
if [ $# -ne 2 ]; then
	echo "Incorrect number of arguments. Usage: <badSites.csv> <file>"
	exit -1
fi

#check if the bad site list file exists
if [ ! -f "$1" ]; then
    echo "$1 doesn't exist"
    exit -2
fi
#check if bad sites file is .csv
if echo "$2" | grep -qv '\.csv$'; then
	echo "bad site file must be a .csv"
	exit -2
fi

#check if the file being checked exists
if [ ! -f "$2" ]; then
    echo "$2 doesn't exist"
    exit -2
fi

########REPLACE $3 with FOUND URL COLUMN?#########
#extract bad urls as list from csv
urls=$(awk -F ',' '{ print $3}' "$2")

#read in the arg file and check each line with the bad url list
while read f; do
	for i in $urls
	do
		#search f for each i
		if echo "$f" | grep -q "$i"; then
			echo "MALICIOUSURL: $i"
			exit -3
		fi
	done
done < $1

#if no bad urls matched with any of the lines, echo clean
echo "CLEAN"

