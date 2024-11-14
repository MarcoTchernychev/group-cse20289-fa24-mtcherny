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

logname="$(date +%F).log"
#add to log time when script started
echo "Script started: $(date)" >> "$4/$logname"
#catch ctrl-c signal using trap, add time to log, then exit
trap {echo "Script exited: $(date)" >> "$4/$logname"; exit 0} SIGINT

#starting inf loop
while true; do    
    archives=$(ls ./scandata/toscan) #getting list of archives to process in toscan dir
 
	#for each archive found in the directory, extract its files and then check that
	#each file within the archive is clean before adding to proper directory and log
	for archive in $(archives); do
		extractoutput=$(sh ae.sh "$archive")
		reasonfile="$archive.reason"

        if [ $? -e 0 ]; then #check that archive is valid (only need to do once)
            #move to quarantine with reason cannot extract, along with .reason file
			echo -e "$archive\nCANNOTEXTRACT" > "$reasonfile"
			mv "$archive" "$3"
			mv "$reasonfile" "$3"
			echo  "$(date), $archive, QUARANTINE, CANNOT EXTRACT" >> "$4/$logname"
			continue
        fi        
 
    	for file in $(ls ./archive); do #looping over the files        
       		urloutput=$(sh sbs.sh $5 "$file") #check for malicious url        
        	sensitiveoutput=$(sh sf.sh "$file") #check for sensitive info       

        	if [[ sensitiveoutput == CLEAN && urloutput==CLEAN ]]; then #if both pass add file to approved 
            	#move to approved
				echo  "$(date), $archive, APPROVE" >> "$4/$logname"
				mv "$archive" "$2"
        	elif [[ sensitiveoutput != CLEAN ]]; then #if contains sensitive info move to quarantine
            #move to quanrantine along with .reason file
				reason="$(tail -n 1 "$sensitiveoutput")"
				echo -e "$file\nSENSITIVE\n$reason" > "$reasonfile"
				echo  "$(date), $archive, QUARANTINE, SENSITIVE, $reason" >> "$4/$logname"
				mv "$file" "$3"
				mv "$reasonfile" "$3"	
        	elif [[ urloutput != CLEAN ]]; then #if contains malicious url move to quarantine
            	#move to quanrantine along with .reason file
				reason="$(tail -n 1 "$urloutput")"
				echo -e "$file\nMALICIOUSURL\n$reason" > "$reasonfile"
				echo  "$(date), $archive, QUARANTINE, MALICIOUSURL, $reason" >> "$4/$logname"
				mv "$file" "$3"
				mv "$reasonfile" "$3"
        	fi
    	done
	done
    sleep 1
done
