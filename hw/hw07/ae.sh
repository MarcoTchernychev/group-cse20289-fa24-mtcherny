#ae.sh
#Alicia Melotik
#amelotik.nd.edu
#Marco Tchernychev
#mtcherny@nd.edu

#!/bin/bash
#set -x
#-o returns the match, '\.' looks for a period, then it takes evrything after the period until the end of the line
#sed, using 's', subs out what's in the first // (which is a leading period), for what is the second //, which is nothing, so take out the leading period /^\./ --> //
filetype=$(echo "$1" | grep -o '\..*$' | sed 's/^\.//')
#echo "$filetype"
isarchives=$(echo $(ls) | grep -o -w 'archives')
#echo "$isarchives"
if [ "$isarchives" != archives ]; then
    echo "archive directory is not present .. creating!"
    mkdir archives
else
    echo "archive directory already present - no need to create"
fi

case $filetype in
    zip)
        echo "Extracting a zip file via unzip"
        unzip "$1" -d ./archives
        ;;
    tar)
        echo "Extracting a tar file"
        tar -x "$1" ./archives
        ;;
    tar.gz)
        echo "Extracting a tar.gz file"
        ;;
esac