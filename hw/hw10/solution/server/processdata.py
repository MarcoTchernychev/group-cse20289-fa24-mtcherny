#processdata.py
#Alicia Melotik
#amelotik@nd.edu
#Marco Tchernychev
#mtcherny@nd.edu

import requests
import statistics

#INPUT: url as a string
#OUTPUT: JSON file as a list
#PURPOSE: take in a url and give a JSON file, if it can't give a JSON file it gives back an error
def fetch(url):
    try:
        response = requests.get(url)
        data = response.json()
        return data
    except:
        print("JSON file does not exist")
        exit(1)

#INPUT: JSON file as a list, filters: date, time, fields (iface (interface), dir (direction), or type (type of test))
#OUTPUT: JSON file as a list
#PURPOSE: filters the JSON file passed in
def filter(json, date, time, field="iface=eth0;dir=downlink;type=iperf"):
    #first filter by field
    year, mon, day = date.split("-")
    fields = field.split(";")
    filteredData = []
    add = 1
    
    for entry in json:
        #find date and time data within curr dictionary
        #print(json)#test
        #print(type(entry)) #test
        #print(entry) #test
        datePart, timePart = entry["timestamp"].split("T")
        curYear, curMon, curDay = datePart.split("-")
        curTime = timePart[0:2]
        if (year == "*" or year == curYear) and (mon == "*" or mon == curMon) and (day == "*" or day == curDay) and (time == "*" or time == curTime):
            for f in fields:
                if "=" in f:
                    key, val = f.split("=")
                    if key == "iface":
                        key = "interface"
                    elif key == "dir":
                        key = "direction"
                    if entry[key] != val:
                        add = 0
                        break
            if add == 1:
                filteredData.append(entry)

        add = 1
            
    return filteredData

#INPUT: filtered list of json data, stat to be found 
#OUTPUT: calculated stat
def calcStat(data, stat):
    dataPts = []
    for entry in data:
        dataPts.append(entry['tput_mbps'])
    
    if stat == "count":
        return len(dataPts)
    elif stat == "mean":
        return statistics.mean(dataPts)
    elif stat == "median":
        return statistics.median(dataPts)
    elif stat == "min":
        return min(dataPts)
    elif stat == "max":
        return max(dataPts)
    elif stat == "stddev":
        if len(dataPts) > 1:
            return statistics.stdev(dataPts)
    

#data = fetch("http://ns-mn1.cse.nd.edu/cse20289-fa24/hw03/data-10.json")
#filtered = filter(data, "*-05-03", "02", "hey")
#print(filtered)
#print(len(filtered))

