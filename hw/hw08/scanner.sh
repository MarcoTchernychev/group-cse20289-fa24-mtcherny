#scanner.sh
#Alicia Melotik
#amelotik@nd.edu
#Marco Tchernychev
#mtcherny@nd.edu

#!/bin/bash
#set -x

#check for correct number of args
if [ $# -ne 5 ]; then
    echo "Incorrect usage. Enter <archives dir> <approved dir> <quarantined dir> <log dir> <malicious url file>"
    exit 1
fi

#check that all args exist
if [ ! -e $1 -o ! -d $1 ]; then echo "$1 is not a valid directory"; exit 1; fi
if [ ! -e $2 -o ! -d $2 ]; then echo "$2 is not a valid directory"; exit 1; fi
if [ ! -e $3 -o ! -d $3 ]; then echo "$3 is not a valid directory"; exit 1; fi
if [ ! -e $4 -o ! -d $4 ]; then echo "$4 is not a valid directory"; exit 1; fi
if [ ! -e $5 -o ! -f $5 ]; then echo "$5 is not a valid file"; exit 1; fi

logname="$(date +%F).log"
#add to log time when script started
echo "Script started: $(date)" >> "$4/$logname"
#catch ctrl-c signal using trap, add time to log, then exit
trap 'echo "Script exited: $(date)" >> "$4/$logname"; exit 0' SIGINT

#starting inf loop
while true; do    
 
	#for each archive found in the directory, extract its files and then check that
	#each file within the archive is clean before adding to proper directory and log
	for archive in $(ls $1); do
		reasonfile="$archive.reason"
		extractoutput=$(sh ./helperscripts/ae.sh "$1$archive")

        if [ $? -ne 0 ]; then #check that archive is valid (only need to do once)
            #move to quarantine with reason cannot extract, along with .reason file
			echo -e "$archive\nCANNOTEXTRACT" > "$reasonfile"
			mv "$1/$archive" "$3"
			mv "$reasonfile" "$3"
			echo  "$(date), $archive, QUARANTINE, CANNOT EXTRACT" >> "$4/$logname"
			continue
        fi   

    	for file in $(find ./archive -type f); do #looping over the files        
       		urloutput=$(sh ./helperscripts/sbs.sh $5 "$file" | tail -n 1) #check for malicious url        
        	sensitiveoutput=$(sh ./helperscripts/sf.sh "$file" | tail -n 1) #check for sensitive info       

        	if [[ "$sensitiveoutput" == CLEAN && "$urloutput" == CLEAN ]]; then #if both pass, check rest of files 
				continue
        	elif [[ "$sensitiveoutput" != CLEAN ]]; then #if contains sensitive info move to quarantine
            #move to quanrantine along with .reason file
				reason="$(echo "$sensitiveoutput")"
				echo -e "$file\nSENSITIVE\n$reason" > "$reasonfile"
				echo  "$(date), $archive, QUARANTINE, SENSITIVE, $reason" >> "$4/$logname"
				mv "$1/$archive" "$3"
				mv "$reasonfile" "$3"
				break	
        	elif [[ "$urloutput" != CLEAN ]]; then #if contains malicious url move to quarantine
            	#move to quanrantine along with .reason file
				reason="$(echo "$urloutput")"
				echo -e "$file\nMALICIOUSURL\n$reason" > "$reasonfile"
				echo  "$(date), $archive, QUARANTINE, MALICIOUSURL, $reason" >> "$4/$logname"
				mv "$1/$archive" "$3"
				mv "$reasonfile" "$3"
				break
        	fi
    	done
		if [[ "$sensitiveoutput" == CLEAN && "$urloutput" == CLEAN ]]; then 
			echo  "$(date), $archive, APPROVE" >> "$4/$logname"
			mv "$1/$archive" "$2"
		fi
		#delete archive directory if it exists so files not from curr archive do not get scanned 
		if [ -e "./archive" ]; then
			rm -r "./archive"
		fi
	done
    sleep 1
done
