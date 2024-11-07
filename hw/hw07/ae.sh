#ae.sh
#Alicia Melotik
#amelotik.nd.edu
#Marco Tchernychev
#mtcherny@nd.edu

#!/bin/bash
#set -x

#check if the doesn't file exists
if [ ! -f "$1" ]; then
    echo "$1 doesn't exist"
    exit -1
fi

#-o returns the match, '\.' looks for a period, then it takes evrything after the period until the end of the line
#sed, using 's', subs out what's in the first // (which is a leading period), for what is the second //, which is nothing, so take out the leading period /^\./ --> //
filetype=$(echo "$1" | grep -o '\..*$' | sed 's/^\.//')

#check if the file is tar, tar.gz, or .zip
if ! echo "$filetype" | grep -qE "zip|tar|tar\.gz"; then
    echo "Not a .zip, .tar, or .tar.gz file"
    exit -1
fi

#check to see if archive is in the directory
isarchive=$(echo $(ls) | grep -o -w 'archive')

#if the grep expression didn't return "archive" make the directory and show the message
if [ "$isarchive" != archive ]; then
    echo "archive directory is not present .. creating!"
    mkdir archive
#if the grep expression did return archive, the directory is present, so display the message
else
    echo "archive directory already present - no need to create"
fi

#based on the file type display the appropiate message and zip/extract accordingly into the archive dir
case $filetype in
    zip)
        echo "Extracting a zip file via unzip"
        unzip -q "$1" -d ./archive
        ;;
    tar)
        echo "Extracting a tar file"
        tar -xf "$1" -C ./archive 2>/dev/null
        ;;
    tar.gz)
        echo "Extracting a tar.gz file"
        tar -xzf "$1" -C ./archive 2>/dev/null
        ;;
esac
