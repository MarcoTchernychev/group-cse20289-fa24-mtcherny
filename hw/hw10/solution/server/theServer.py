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
#PURPOSE: takes in a message from the client, if it's invalid it prints an error and sends it to the client, then prnts out that the error was sent to the client
def checkCmnds(message):
    validStat = re.compile(r'^(count|mean|median|min|max|stddev|list)$')
    validDate = re.compile(r'^(?:\*|(?:20(1[0-9]|2[0-4])|\*)-(?:0[1-9]|1[0-2]|\*)-(?:0[1-9]|[12][0-9]|3[01]|\*))$')
    validTime = re.compile(r'^(?:\*|0[0-9]|1[0-9]|2[0-3])$')
    validFilter = re.compile(r'^(iface=(eth0|wlan0);dir=(downlink|uplink);type=iperf)$')
    commands = message.split(', ')
    if len(commands) == 1:
        if commands[0] == "exit" or commands[0] == "more":
            return True
        else:
            print("error - unrecognized argument")
            socket.send_string("failure, unrecognized argument")
            print("SENT: failure, unrecognized argument")
            return False
    elif len(commands) == 3:
        stat = commands[0]
        date = commands[1]
        time = commands[2]
        if not re.fullmatch(validStat, stat):
            print("error - invalid stat argument")
            socket.send_string("failure, invalid stat argument")
            print("SENT: failure, invalid stat argument")
            return False
        if not re.fullmatch(validDate, date):
            print("error - invalid date argument")
            socket.send_string("failure, invalid date argument")
            print("SENT: failure, invalid date argument")
            return False
        if not re.fullmatch(validTime, time):
            print("error - invalid time argument")
            socket.send_string("failure, invalid time argument")
            print("SENT: failure, invalid time argument")
            return False
        return True
    elif len(commands) == 4:
        stat = commands[0]
        date = commands[1]
        time = commands[2]
        filter = commands[3]
        if not re.fullmatch(validStat, stat):
            print("error - invalid stat argument")
            socket.send_string("failure, invalid stat argument")
            print("SENT: failure, invalid stat argument")
            return False
        if not re.fullmatch(validDate, date):
            print("error - invalid date argument")
            socket.send_string("failure, invalid date argument")
            print("SENT: failure, invalid date argument")
            return False
        if not re.fullmatch(validTime, time):
            print("error - invalid time argument")
            socket.send_string("failure, invalid time argument")
            print("SENT: failure, invalid time argument")
            return False
        if not re.fullmatch(validFilter, filter):
            print("error - invalid filter argument")
            socket.send_string("failure, invalid filter argument")
            print("SENT: failure, invalid filter argument")
            return False
        return True
    else:
        print("error - not enough arguments")
        socket.send_string("failure, not enough arguments")
        print("SENT: failure, not enough arguments")
        return False

#INPUT: JSON file of the list
#OUTPUT: content of one line of the JSON file formatted as: success, #of lines remaining, key (eg. "timestamp"), value (eg. "the actual timestamp"), ...
#PURPOSE: check that there are lines remaining to do "more" on, and if there are, send the data... otherwise send a failure
def more(json):
    if len(json) == 0: #if no data left to do more on
        socket.send_string("failure, no more data to send")
        print("SENT: failure, no more data to send")
    else:
        line = json.pop[0]


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

lastcmnd = '' #holder for the last command (if more is called we want to make sure list was the last command)
lastjson = [] #holder for the last json

while True:
    try:
        print("Waiting for a new command") #wait for next command from client
        message = socket.recv() #recieve command
        print(f"RCVD: {message}") #notify user that command was recieved
        if checkCmnds(message) == False: #check that command is valid - if it isn't then notify user and continue
            continue
        
        data = processdata.fetch(url) #get the data
        commands = message.split(', ')

        if commands[0] == "exit": #if exit message is quit then quit
            print("SENT: success, exiting") 
            exit()
        if commands[0]=="more": #if more command
            #check that list was called last
            if lastcmnd != "list":
                print("error - must do list first")
                socket.send_string("failure, didn't do list yet")
                print("SENT: failure, didn't do list yet")
                continue
            #send over one line of the JSON along with the print message for the server
            elif lastcmnd == "list":
                ###MAKE A FUNC THAT RETURNS THE PROPER SEND MESSAGE AND TAKES A LINE OUT OF THE LIST (MAYBE POP)
                pass     
   
        lastcmnd = commands[0] #getting the last command so more can check that list was called last

        if len(commands)==3:
            filtereddata = processdata.filter(commands[0], commands[1], commands[2])
            result = processdata.calcStat(filtereddata, commands[0])
            if commands[0] == "list":
                lastjson = filtereddata #store this for more command
                socket.send_string(f'success, {len(filtereddata)}') #send the count for the filtered data
                print(f'SENT: success, {len(filtereddata)}') #and make the print stmnt
            else:
                print(f'{commands[0]} requested - {len(filtereddata)} records')
                socket.send_string(f'success, {commands[0]}, {result}')
                print(f'SENT: success, {commands[0]}, {result}')
        else:
            filtereddata = processdata.filter(commands[0], commands[1], commands[2], commands[3])
            result = processdata.calcStat(filtereddata, commands[0])
            if commands[0] == "list":
                lastjson = filtereddata #store this for more command
                socket.send_string(f'success, {len(filtereddata)}') #send the count for the filtered data
                print(f'SENT: success, {len(filtereddata)}') #and make the print stmnt
            else:
                print(f'{commands[0]} requested - {len(filtereddata)} records')
                socket.send_string(f'success, {commands[0]}, {result}')
                print(f'SENT: success, {commands[0]}, {result}')

    except KeyboardInterrupt:
        print("Goodbye")
        exit()
