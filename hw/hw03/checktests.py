#Marco Tchernycheb
#mtcherny@nd.edu
import argparse
import requests
import json
import numpy as np

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
#INPUT: unflitered and unsorted JSON file as a list
#OUTPUT: new filtered and sorted JSON file as a list
#PURPOSE: eliminate all data entries that don't have downlink for direction and iperf for type, the filter based on timestamp
def filterSort(data):
    filtered = [entry for entry in data if (entry["direction"]=="downlink" and entry["type"]=="iperf")]
    filteredsorted =  sorted(filtered, key=lambda x:x["timestamp"])
    return filteredsorted
#INPUT: JSON file as a list with unfiltered values, and parameters for what you want to filter for
#OUPUT: JSON file as a list with entries that conatin the values filtered for
#PURPOSE: return a list of all data points that satisfy the requested filtering (ie. that include the parameters)
def filterit(data, month = 5, year = 2024, interface = "eth0"):
    if month>9: #accounting for the fact that one digit integers are written as "05"
        return list(filter(lambda entry: (entry["interface"]==interface and entry["timestamp"][:4]==str(year) and entry["timestamp"][5:7]==str(month)), data))
    else:
        return list(filter(lambda entry: (entry["interface"]==interface and entry["timestamp"][:4]==str(year) and entry["timestamp"][6:7]==str(month)), data))
#INPUT: JSON file as a list and interface to analyze (eth0 or wlan0)
#OUTPUT: dictionary for stats for that dataset
#PURPOSE: take in data points and for a specific interface find data (specified on github)
def analyze(data, interface):
    data = list(filter(lambda entry: entry["Interface"] == interface, data))
    tput_list = [entry["tput_mbps"] for entry in data]
    dict =  {"Period": data[-1]["timestamp"] - data[0]["timestamp"], 
             "Interface" : interface, 
             "Num Points": len(data), 
             "Min": min(tput_list), 
             "Max": max(tput_list), 
             "Mean": mean(tput_list), 
             "Median": median(tput_list), 
             "Std Dev": stdev(tput_list), 
             "10th Percentile": np.percentile(tput_list,10), 
             "90th Percentile": np.percentile(tput_list,90)}

###START OF FETCHING###
parser = argparse.ArgumentParser()
parser.add_argument("url", type=str)
args = parser.parse_args()
url = args.url
###START OF FILTERING###
data = fetch(url)
fsdata = filterSort(data)
filtered = filterit(fsdata)

###TESTS###
#print(type(data)) #list
#print(data) #list
#data_string = json.dumps(data, indent = 4)
#print(data_string) #nice looking string
#print("\n############################################\n")
#fsdata_string = json.dumps(fsdata, indent = 4)
#print(fsdata_string)
#print("\n############################################\n")
#filtered_string = json.dumps(filtered, indent = 4)
#print(filtered_string)