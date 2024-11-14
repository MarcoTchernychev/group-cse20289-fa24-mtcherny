#scanner.sh
#Alicia Melotik
#amelotik@nd.edu
#Marco Tchernychev
#mtcherny@nd.edu

#!/bin/bash
set -x

#check for correct number of args
if [ $# -ne 5 ]; then
    echo "Incorrect usage. Enter <archives dir> <approved dir> <quarantined dir> <log dir> <malicious url file>"
    exit 1
fi

#check that all args exist
if [ ! -e $1]; then echo "$1 does not exist"; exit 1; fi
if [ ! -e $2]; then echo "$2 does not exist"; exit 1; fi
if [ ! -e $3]; then echo "$3 does not exist"; exit 1; fi
if [ ! -e $4]; then echo "$4 does not exist"; exit 1; fi
if [ ! -e $5]; then echo "$5 does not exist"; exit 1; fi

#starting inf loop
while true; do    
    files=$(ls ./scandata/toscan) #getting list of files in toscan dir 
	#is this list of archives? when do we extract the archives?
	logname="$(date +%F).log"
 
    for file in $(files); do #looping over the files        
        urloutput=$(sh sbs.sh $5 "$file") #check for malicious url        
		reasonfile="$file.reason"
        if [ $? -e 0 ]; then #check that file is valid (only need to do once)
            #move to quarantine with reason cannot extract, along with .reason file
			mv "$file" "$3"
			echo -e "$file\nCANNOTEXTRACT" > "$reasonfile"
			mv "$reasonfile" "$3"
        fi        
        sensitiveoutput=$(sh sf.sh "$file") #check for sensitive info       
        if [[ sensitiveoutput == CLEAN && urloutput==CLEAN ]]; then #if both pass add file to approved 
            #move to approved
			mv "$file" "$2"
        elif [[ sensitiveoutput != CLEAN ]]; then #if contains sensitive info move to quarantine
            #move to quanrantine along with .reason file
			mv "$file" "$3"
			echo -e "$file\nSENSITIVE\n$(tail -n 1 "$sensitiveoutput")" > "$reasonfile"
			mv "$reasonfile" "$3"
        elif [[ urloutput != CLEAN ]]; then #if contains malicious url move to quarantine
            #move to quanrantine along with .reason file
			mv "$file" "$3"
			echo -e "$file\nMALICIOUSURL\n$(tail -n 1 "$urloutput")" > "$reasonfile"
			mv "$reasonfile" "$3"
        fi
    done
    sleep 1
done
