#mix.sh
#Alicia Melotik
#amelotik@nd.edu
#Marco Tchernychev
#mtcherny@nd.edu

#!/bin/bash
#set -x

sleep 2
#bad
cp ./archives/example-targz.tar.gz ~/repos/group-cse20289-fa24-mtcherny/hw/hw08/scandata/toscan
sleep 2
#good
cp /archives/good.tar ~/repos/group-cse20289-fa24-mtcherny/hw/hw08/scandata/toscan
sleep 2
#bad
cp ./archives/SSN.zip ~/repos/group-cse20289-fa24-mtcherny/hw/hw08/scandata/toscan
sleep 2
#good
cp ./archives/good3.tar.gz ~/repos/group-cse20289-fa24-mtcherny/hw/hw08/scandata/toscan
sleep 2