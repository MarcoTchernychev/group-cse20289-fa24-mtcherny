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


outputc=$(./client "$hostname" "number")
if [[ "$outputc" == "Error: port must be an integer number" ]]; then
	echo "Successfully detected non-integer port number arg"
fi

#run client with assortment of test cases and capture all output
outputc=$(echo -e "count, *-*-*, 02\nmean, 2024-05-*, *, iface=eth0;dir=uplink;type=iperf\nincorrect, input\nincorrect input\nexit\n" | ./client "$hostname" "$portnum")

#check if first commant (count) ran successfully
if [[ $(echo "$outputc" | head -n 5) ==  "Connecting to server on port $portnum
	Successfully connected on port $portnum
Waiting for message (stat, date, time, {filter})/more/exit:
Sending message: count, *-*-*, 02
Received: success, count, 189" ]]; then
	echo "C client successfully outputed count of 189 records"
fi

#check if next cmd (mean w/ specified filter) ran successfully
if [[ $(echo "$outputc" | sed -n '6,8p') == "Waiting for message (stat, date, time, {filter})/more/exit:
Sending message: mean, 2024-05-*, *, iface=eth0;dir=uplink;type=iperf
Received: success, mean, 23.36637723954102" ]]; then
	echo "C client successfully outputed mean of 23.26..."
fi

#check if next command (invalid # of input args) ran successfully
if [[ $(echo "$outputc" | sed -n '9,10p') == "Waiting for message (stat, date, time, {filter})/more/exit:
Message formatted incorrectly" ]]; then
	echo "C client successfully caught incorrect number of input commands"
fi

#check if final command (invalid single command) ran successfully
if [[ $(echo "$outputc" | tail -n 3) == "Waiting for message (stat, date, time, {filter})/more/exit:
Message formatted incorrectly
Waiting for message (stat, date, time, {filter})/more/exit:" ]]; then
	echo "C client successfully caught invalid input command"
fi

make clean > /dev/null 2>&1

