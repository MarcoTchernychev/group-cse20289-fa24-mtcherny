#theServer.py
#Alicia Melotik
#amelotik@nd.edu
#Marco Tchernychev
#mtcherny@nd.edu
import processdata
import re
import sys
import zmq
import time
import json

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
            print(f'error - unrecognized single command {commands[0]}')
            socket.send_string(f'failure, unrecognized single command {commands[0]}')
            print(f'SENT: failure, unrecognized single command {commands[0]}')
            return False
    elif len(commands) == 3:
        stat = commands[0]
        date = commands[1]
        time = commands[2]
        if len(time)==1 and time!='*': #single digit times should have a 0 in front of them
            time="0"+time
        if not re.fullmatch(validStat, stat):
            print(f"error - invalid stat command {commands[0]}")
            socket.send_string(f"failure, invalid stat command {commands[0]}")
            print(f"SENT: failure, invalid stat command {commands[0]}")
            return False
        if not re.fullmatch(validDate, date):
            print(f"error - invalid date command {commands[1]}")
            socket.send_string(f"failure, invalid date command {commands[1]}")
            print(f"SENT: failure, invalid date command {commands[1]}")
            return False
        if not re.fullmatch(validTime, time):
            print(f"error - invalid time command {commands[2]}")
            socket.send_string(f"failure, invalid time command {commands[2]}")
            print(f"SENT: failure, invalid time command {commands[2]}")
            return False
        return True
    elif len(commands) == 4:
        stat = commands[0]
        date = commands[1]
        time = commands[2]
        filter = commands[3]
        if len(time)==1 and time!='*': #single digit times should have a 0 in front of them
            time="0"+time
        if not re.fullmatch(validStat, stat):
            print(f"error - invalid stat command {commands[0]}")
            socket.send_string(f"failure, invalid stat command {commands[0]}")
            print(f"SENT: failure, invalid stat command {commands[0]}")
            return False
        if not re.fullmatch(validDate, date):
            print(f"error - invalid date command {commands[1]}")
            socket.send_string(f"failure, invalid date command {commands[1]}")
            print(f"SENT: failure, invalid date command {commands[1]}")
            return False
        if not re.fullmatch(validTime, time):
            print(f"error - invalid time command {commands[2]}")
            socket.send_string(f"failure, invalid time command {commands[2]}")
            print(f"SENT: failure, invalid time command {commands[2]}")
            return False
        if not re.fullmatch(validFilter, filter):
            print(f"error - invalid filter command {commands[3]}")
            socket.send_string(f"failure, invalid filter command {commands[3]}")
            print(f"SENT: failure, invalid filter command {commands[3]}")
            return False
        return True
    else:
        print("error - wrong number of commands")
        socket.send_string("failure, wrong number of commands")
        print("SENT: failure, wrong number of commands")
        return False

#INPUT: JSON file of the list
#OUTPUT: none, sends appropiate message and prints that it sent
#PURPOSE: check that there are lines remaining to do "more" on, and if there are, send the data... otherwise send a failure
def more(json):
    if len(json) == 0: #if no data left to do more on
        socket.send_string("failure, no more data to send")
        print("SENT: failure, no more data to send")
    else:
        #print(json)#test
        #print(type(json))#test
        line = json.pop(0) #pop one line of the json
        returnstr = '' #holder for the line of data
        for field, value in line.items():
            returnstr += f'{field}, {value}, ' #appending the field and value to the line
        returnstr = returnstr[0:-2] #getting rid of trailing ', '
        socket.send_string(f'success, {len(json)}, {returnstr}') #sending the string
        print(f'SENT: success, {len(json)}, {returnstr}') #printing success

def regular():

    lastcmnd = '' #holder for the last command (if more is called we want to make sure list was the last command)
    lastjson = [] #holder for the last json

    while True:
        try:
            print("Waiting for a new command") #wait for next command from client
            message = socket.recv() #recieve command
            message = message.decode('utf-8').strip()
            print(f"RCVD: {message}") #notify user that command was recieved
            if("nice" in message): #if nice is found in message, start NiceListMore that accounts for nice being in front of every stat.
                NiceListMore(message)
                exit()
            if checkCmnds(str(message)) == False: #check that command is valid - if it isn't then notify user and continue
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
                elif lastcmnd == "list":
                    more(lastjson) #a func that sends the proper line and shortens the json then prints what it sent, also checks that more command is valid
                    continue     
            
            lastcmnd = commands[0] #getting the last command so more can check that list was called last

            if len(commands[2])==1 and commands[2]!='*': #single digit times should have a 0 in front of them
                commands[2]="0"+commands[2]

            if len(commands)==3:
                filtereddata = processdata.filter(data, commands[1], commands[2])
                if filtereddata == []: #check if filtered data is empty becuase then stats will get an error
                    socket.send_string("filtered out all data, count is 0")
                    print("SENT: filtered out all data, count is 0")
                    continue
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
                filtereddata = processdata.filter(data, commands[1], commands[2], commands[3])
                if filtereddata == []: #check if filtered data is empty becuase then stats will get an error
                    socket.send_string("filtered out all data, count is 0")
                    print("SENT: filtered out all data, count is 0")
                    continue
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
            print("\nGoodbye")
            time.sleep(1)
            exit()

def NiceListMore(message):
    lastcmnd = '' #holder for the last command (if more is called we want to make sure list was the last command)
    lastjson = [] #holder for the last json
    while True:
        try:
            message = message[4:]
            if message == "":
                message = socket.recv() #recieve command
                message = message.decode('utf-8').strip()
                continue
                
            print(f"RCVD: {message}") #notify user that command was recieved
            if checkCmnds(str(message)) == False: #check that command is valid - if it isn't then notify user and continue
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
                elif lastcmnd == "list":
                    socket.send_string(f'{json.dumps(lastjson.pop(0), indent=4)}') #a func that sends the proper line and shortens the json then prints what it sent, also checks that more command is valid
                    continue     
            
            lastcmnd = commands[0] #getting the last command so more can check that list was called last     

            if len(commands[2])==1 and commands[2]!='*': #single digit times should have a 0 in front of them
                commands[2]="0"+commands[2]

            if len(commands)==3:
                filtereddata = processdata.filter(data, commands[1], commands[2])
                if filtereddata == []: #check if filtered data is empty becuase then stats will get an error
                    socket.send_string("filtered out all data, count is 0")
                    print("SENT: filtered out all data, count is 0")
                    continue
                result = processdata.calcStat(filtereddata, commands[0])
                if commands[0] == "list":
                    lastjson = filtereddata #store this for more command
                    socket.send_string(f'success, {len(filtereddata)}') #send the count for the filtered data
                    print(f'SENT: success, {len(filtereddata)}') #and make the print stmnt
                else:
                    print(f'{commands[0]} requested - {len(filtereddata)} records')
                    socket.send_string(f'''
                                            +-----------------------+
                                            | SUCCESS!              |                        
                                            +-----------------------+
                                            | {commands[0]} : {result:<15.2f}|
                                            +-----------------------+
                                            ''')
                    print(f'SENT: success, {commands[0]}, {result}')
            else:
                filtereddata = processdata.filter(data, commands[1], commands[2], commands[3])
                if filtereddata == []: #check if filtered data is empty becuase then stats will get an error
                    socket.send_string("filtered out all data, count is 0")
                    print("SENT: filtered out all data, count is 0")
                    continue
                result = processdata.calcStat(filtereddata, commands[0])
                if commands[0] == "list":
                    lastjson = filtereddata #store this for more command
                    socket.send_string(f'success, {len(filtereddata)}') #send the count for the filtered data
                    print(f'SENT: success, {len(filtereddata)}') #and make the print stmnt
                else:
                    print(f'{commands[0]} requested - {len(filtereddata)} records')
                    socket.send_string(f'''
                                            +-----------------------+
                                            | SUCCESS!              |                        
                                            +-----------------------+
                                            | {commands[0]} : {result:<15.2f}|
                                            +-----------------------+
                                            ''')
                    print(f'SENT: success, {commands[0]}, {result}')
            
            print("Waiting for a new command") #wait for next command from client
            message = socket.recv() #recieve command
            message = message.decode('utf-8').strip()

        except KeyboardInterrupt:
            print("\nGoodbye")
            time.sleep(1)
            exit()

#check for correct number of command line args
if len(sys.argv)!=3:
    print("incorrect usage, run as: python3 theServer.py <url> <server port>")
    exit()

url = sys.argv[1]
try:
    serverPort = int(sys.argv[2]) #40645
except:
    print("make sure the port is the 2nd argument")
    exit()

context = zmq.Context()
socket = context.socket(zmq.REP)
try: 
    socket.bind("tcp://*:" + str(serverPort)) #Binds the socket to a specific address and port. ZeroMQ uses tcp:// for TCP sockets. The * means it will listen on all available network interfaces.
    print(f'Server started successfully - listening on Port {serverPort}!')
except:
    print(f'Failed to bind on port {serverPort}')
    exit()
regular()
