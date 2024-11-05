#ae.sh
#Alicia Melotik
#amelotik.nd.edu
#Marco Tchernychev
#mtcherny@nd.edu

#!/bin/bash
#set -x

#getting the actual file
file=$(echo "$1" | grep -o '\/.*$' | sed 's/^\///')
#check to see that file being passed is a txt file
filetype=$(echo "$1" | grep -o '\..*$' | sed 's/^\.//')
if [ "$filetype" != txt ]; then
    echo "$file not a txt file"
    exit -1
fi

#check to see if the file exists in the sensitive dir
isfile=$(echo $(ls ./sensitive/) | grep -o -w "$file")
#if the grep expression didn't return the file display a message
if [ "$isfile" != "$file" ]; then
    echo "$file does not exist in sensitive"
    exit -1
fi

text=$(read "./$1")