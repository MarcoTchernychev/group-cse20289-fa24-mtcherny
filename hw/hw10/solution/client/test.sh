#test.sh
#Alicia Melotik
#amelotik@nd.edu
#Marco Tchernychev
#mtcherny@nd.edu

#!/bin/bash
#set -x

#first, make c client using Makefile
make clean > /dev/null 2>&1
make client > /dev/null 2>&1

hostname=localhost
portnum=40645

#test for invalid input/error checking
outputc=$(./client "$hostname")
if [[ "$outputc" == "Usage: ./client hostname portnumber" ]]; then
	echo "Successfully detected incorrect number of args"
fi
# exit code -2

outputc=$(./client "$hostname" "number")
if [[ "$outputc" == "Error: port must be an integer number" ]]; then
	echo "Successfully detected non-integer port number arg"
fi

# $? is exit value of last cmd run
#o exit code -1

python3 ../server/theServer.py "http://ns-mn1.cse.nd.edu/cse20289-fa24/hw03/data-all.json" "$portnum" &

echo -e "count, *-*-*, 02\nexit\n" | ./client "$hostname" "$portnum" 

echo -e "incorrect, input\nexit\n" | ./client "$hostname" "$portnum"

echo -e "incorrect input\nexit\n" | ./client "$hostname" "$portnum"

#outputc=$(./client "$hostname" "$portnum" | tee temp_c.txt &)
#echo $outputc
#"\tSuccessfully connected on port $portnum\nWaiting for message (stat, date, time, {filter})/more/exit:\n"


#python3 theServer.py "http://ns-mn1.cse.nd.edu/cse20289-fa24/hw03/data-all.json" "$portnum" | tee temp_py.txt &
#echo $outputpy
#'Server started successfully - listening on Port "$portnum"!' Wating for a new command


