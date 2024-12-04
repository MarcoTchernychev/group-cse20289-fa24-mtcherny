#processdata.py
#Alicia Melotik
#amelotik@nd.edu
#Marco Tchernychev
#mtcherny@nd.edu

import requests

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
        curYear, curMon, curDay = entry["timestamp"].split("-")[0:3]
        curTime = curDay[4:6]
        curDay = curDay[0:2]
        if (year == "*" or year == curYear) and (mon == "*" or mon == curMon) and (day == "*" or day == curDay) and (time == "*" or time == curTime):
            for f in fields:
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

#data = fetch("http://ns-mn1.cse.nd.edu/cse20289-fa24/hw03/data-10.json")
#filtered = filter(data, "*-*-*", "*")
#print(filtered)
#print(len(filtered))

