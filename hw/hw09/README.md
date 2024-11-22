Alicia Melotik
amoletik@nd.edu
Marco Tchernychev
mtcherny@nd.edu

TASK 4:
Alicia: Line 9 in packet.h: increased the macro PKT_SIZE_LIMIT from 1500 to 2500 

TASK 5
Marco: Line 65 in main.c: free theInfo.FileName because strdup dynamically allocated it
Alicia: Line 66 in main.c: free big table
Alicia: Line 222 in pcap-process.c: uncommented to discardPacket free the struct