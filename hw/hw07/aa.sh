#aa.sh
#Alicia Melotik
#amelotik@nd.edu
#Marco Tchernychev
#mtcherny@nd.edu

#!/bin/bash
#set -x

#check if archive file provided as argument
if [ $# -ne 2 ]; then
	echo "Usage: $0 <file-to-extract> <badsites-file>"
	exit -1
fi
if [ ! -f "$1" ]; then
	echo "Error: archive file to extract $1 could not be found"
	exit -1
fi
if [ ! -f "$2" ]; then
	echo "Error: bad sites file $2 could not be found"
	exit -1
fi
if [ $# -e 4 ]; then
	if [[ "$3" != "-ad" ]]; then
		echo "Usage: $0 <file-to-extract> <badsites-file> [-ad X]"
		exit -1
	fi
	if [[ "$4" =~ ^(?![0-3]$).+$ ]]; then
		echo "Error: archive depth can only be an int from 0 to 3"
		exit -1
	fi

fi

#first, extract the archive and find files
sh ae.sh "$1" >/dev/null
files=$(find ./archive -type f)

#next, check the extracted files for bad urls
#then check for sensitive info
for f in $files
do
	#skip files starting with ._
	if [[ "$f" == *"/._"* ]]; then
		continue
	fi	
	
	badSitesResult=$(./sbs.sh $2 $f)
	if [[ $? -ne 0 ]]; then
		echo "$badSitesResult"
		rm -r archive/
		exit -2
	fi
	sensitiveResult=$(./sf.sh $f)
	if [[ $? -ne 0 ]]; then
		echo "$sensitiveResult" | tail -n1
		rm -r archive/
		exit -3
	fi
done

#if nothing was triggered, echo CLEAN and delete archive directory
echo "CLEAN"
rm -r archive/

