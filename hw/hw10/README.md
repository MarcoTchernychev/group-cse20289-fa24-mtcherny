Alicia Melotik

amelotik@nd.edu

Marco Tchernychev

mtcherny@nd.edu

For the format of the (stat, date, time, {filter}) request, the optional filter requires all three fields to be specified-like [iface=(eth0|wlan0);dir=(downlink|uplink);type=iperf]

For bb and bbf, if using wildcard, must escape * using a backslash, ie: \*

For bb, send the filter in quotes becuase ; is a special char, ie: "iface=eth0;dir=uplink;type=iperf"

For task 5, we got bbf to work and print the stat commands nicely. it uses listmore to continuously call more to list all the records. It works the same as bb with the conditions like -query.

