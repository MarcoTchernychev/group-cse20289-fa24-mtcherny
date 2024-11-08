#ae.sh
#Alicia Melotik
#amelotik.nd.edu
#Marco Tchernychev
#mtcherny@nd.edu

#!/bin/bash
#set -x

#check for proper number or args
if [ $# -ne 1 ]; then
	echo "Incorrect number of arguments. Usage: $0 <file>"
	exit -1
fi

#getting the actual file
file=$(echo "$1" | grep -o '\/.*$' | sed 's/^\///')

#check to see that file being passed is a txt file (commented out -- no need(?))
#filetype=$(echo "$1" | grep -o '\..*$' | sed 's/^\.//')
#if [ "$filetype" != txt ]; then
#    echo "$file not a txt file"
#    exit -1
#fi

#check to see if the file exists in the sensitive dir
#isfile=$(echo $(ls ./sensitive/) | grep -o -w "$file")
#if the grep expression didn't return the file display a message
#if [ "$isfile" != "$file" ]; then
#    echo "$file does not exist in sensitive"
#    exit -1
#fi

echo "scanning for sensitive information"
echo "file to scan: $1"

for word in "$file"; do
    #see if there's a sensitive info match in the word
    match=$(echo "$word" | grep -Eo "\*SENSITIVE\*|[0-9]{3}-[0-9]{2}-[0-9]{4}|9022[0-9]{5}") 
    #if the match isn't empty go through and check to see what it matched to and print appropiate message
    if [ "$match" != ' ' ]; then
        if [ "$match" == *SENSITIVE* ]; then
            echo "SENSITIVE, MARKED SENSITIVE"
            exit -1
        fi
        if echo "$match" | grep -Eq "[0-9]{3}-[0-9]{2}-[0-9]{4}"; then
            echo "SENSITIVE, SSN"
            exit -1
        fi
        if echo "$match" | grep -Eq "9022[0-9]{5}"; then
            echo "SENSITIVE, STUDENTID"
            exit -1
        fi
    fi
done
#if it passed the regex matches, print CLEAN
echo "CLEAN"
