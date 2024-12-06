#test.sh
#Alicia Melotik
#amelotik@nd.edu
#Marco Tchernychev
#mtcherny@nd.edu

#!/bin/bash
#set -x

#first, make c client
make clean
make client

hostname=localhost
portnum=40645

./client localhost $hostname $portnum

