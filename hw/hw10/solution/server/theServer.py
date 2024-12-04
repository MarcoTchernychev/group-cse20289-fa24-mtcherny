#theServer.py
#Alicia Melotik
#amelotik@nd.edu
#Marco Tchernychev
#mtcherny@nd.edu
import processdata
import re
import sys
import zmq

#INPUT: message as a string
#OUTPUT: true or false, and prints if bad
#PURPOSE: take in a url and give a JSON file, if it can't give a JSON file it gives back an error
def checkCmnds(message):
    validStat = re.compile(r'(count|mean|median|min|max|stddev|list)') #confused about how exit and more will be sent
    validDate = re.compile(r'')
    validTime = re.compile(r'[0-23]|\*')
    validFilter = re.compile(r'iface=(eth0|wlan0);dir=(downlink|uplink);type=iperf')
    commands = message.split(', ')
    if len(commands) == 1:
        if commands[0] == "exit" or commands[0] == "more":
            return True
    elif len(commands) == 4:
        stat = commands[0]
        data = commands[1]
        time = commands[2]
        filter = commands[3]
        if stat
    else:
        print("Not enough arguments")
        return False
    



url = sys.argv[1]
serverPort = int(sys.argv[2]) #40645

context = zmq.Context()
socket = context.socket(zmq.REP)
try: 
    socket.bind("tcp://*:" + str(serverPort)) #Binds the socket to a specific address and port. ZeroMQ uses tcp:// for TCP sockets. The * means it will listen on all available network interfaces.
    print(f'Server started successfully - listening on Port {serverPort}!')
except:
    print(f'Failed to bind on port {serverPort}')
    exit()

while True:
    try:
        #Wait for next request from client
        print("Waiting for a new command")
        message = socket.recv()
        print(f"RCVD: {message}")  
        #regex func valid requests


    except KeyboardInterrupt:
        print("Goodbye")
        exit()
