Alicia Melotik

amelotik@nd.edu

Marco Tchernychev

mtcherny@nd.edu

For the format of the (stat, date, time, {filter}) request, the optional filter requires all three fields to be specified-like [iface=(eth0|wlan0);dir=(downlink|uplink);type=iperf]

For bb and bbf, if using wildcard, must escape * using a backslash, ie: \*

For bb, send the filter in quotes becuase ; is a special char, ie: "iface=eth0;dir=uplink;type=iperf"