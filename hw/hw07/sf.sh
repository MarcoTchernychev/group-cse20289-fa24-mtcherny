#ae.sh
#Alicia Melotik
#amelotik.nd.edu
#Marco Tchernychev
#mtcherny@nd.edu

#!/bin/bash
#set -x

#check to see that filebeing passed is a txt file
filetype=$(echo "$1" | grep -o '\..*$' | sed 's/^\.//')
echo "$filetype"
if [ "$filetype" != txt ]; then
    echo "not a txt file"
fi

#check to see if the exists in the sensitive dir (need to work on this)
file=$(echo $(ls ./sensitive/) | grep -o -w '"$1"')
echo "$file"
if [ "$file" != "$1" ]; then
    echo "$1 does not exist in sensitive"
fi