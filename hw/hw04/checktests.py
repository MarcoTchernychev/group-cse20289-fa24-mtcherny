#Marco Tchernycheb
#mtcherny@nd.edu
import argparse
import requests
import json
import statistics
import numpy as np
import plotdata
import createreport
import os

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
    if int(month)>9: #accounting for the fact that one digit integers are written as "05"
        return list(filter(lambda entry: (entry["interface"]==interface and entry["timestamp"][:4]==str(year) and entry["timestamp"][5:7]==str(month)), data))
    else:
        return list(filter(lambda entry: (entry["interface"]==interface and entry["timestamp"][:4]==str(year) and entry["timestamp"][6:7]==str(month)), data))
#INPUT: JSON file as a list and interface to analyze (eth0 or wlan0)
#OUTPUT: dictionary for stats for that dataset
#PURPOSE: take in data points and for a specific interface find data (specified on github)
def analyze(data, interface):
    data = list(filter(lambda entry: entry["interface"] == interface, data))
    tput_list = [entry["tput_mbps"] for entry in data]
    #start = data[0]["timestamp"].split(['-','T', ':'])
    #end = data[-1]["timestamp"].split(['-','T',':'])
    dict =  {"Period": f"{data[0]['timestamp'][:4]}-{data[0]['timestamp'][5:7]}", 
             "Interface" : interface, 
             "Num Points": len(data), 
             "Min": round(min(tput_list),2), 
             "Max": round(max(tput_list),2), 
             "Mean": round(statistics.mean(tput_list),2), 
             "Median": round(statistics.median(tput_list),2), 
             "Std Dev": round(statistics.stdev(tput_list),2), 
             "10th Percentile": round(np.percentile(tput_list, 10),2), 
             "90th Percentile": round(np.percentile(tput_list, 90),2)}
    #if args.all:
    #    dict["Period"] = "ALL"
    return dict
#INPUT: dictionary with stats
#OUTPUT: a nice print
#PURPOSE: make dict readable
def output(dict):
    for key in dict:
        print(f"{key}: {dict[key]}")

#INPUT: year, month, txtfile, url, prepend (prepend is put at start of name for any file done in a task)
#OUTPUT: report docx
#PURPOSE: make everything that would go in main into a single function (modified functionality for hw04)
def doItAll(year,month, txtfile, url, prepend):
    ###SETING UP WORKING DIR###
    directory = os.getcwd()
    ###IF DOCX ALREADY EXISTS###
    for file_name in os.listdir(directory):
        if file_name == f"{year}-{month}-Wired.docx":
            print("will overwrite existing docx files")
    ###MONTH NUM : DAY NUM DICT###
    month_days = {
        1: 31,  # January
        2: 28,  # February
        3: 31,  # March
        4: 30,  # April
        5: 31,  # May
        6: 30,  # June
        7: 31,  # July
        8: 31,  # August
        9: 30,  # September
        10: 31,  # October
        11: 30,  # November
        12: 31   # December
    }
    ###FETCHING###
    data = fetch(url)
    ###FILTER AND SORT###
    fsdata = filterSort(data)
    ###FILTER FOR WIRED AND WIFI###
    filtered_eth0 = filterit(fsdata, month, year)
    if len(filtered_eth0)==0:
        print("the year / month requested has no data after filtering")
        exit(1)
    filtered_wlan0 = filterit(fsdata, month, year, "wlan0")
    if len(filtered_wlan0)==0:
        print("the year / month requested has no data after filtering")
        exit(1)
    ###MAKE DATA DICTIONARIES FOR WIRED AND WIFI###
    dict_eth0 = analyze(filtered_eth0, "eth0")
    dict_wlan0 = analyze(filtered_wlan0, "wlan0")
    ###MAKE PLOTS###
    plotdata.createPlot(plotdata.dailyAvg(filtered_eth0, month_days[int(month)]), prepend+"eth0.png")
    plotdata.createPlot(plotdata.dailyAvg(filtered_wlan0, month_days[int(month)]), prepend+"wlan0.png")
    ###MAKE REPORTS###
    createreport.makeReport(txtfile, dict_eth0, prepend+"eth0.png", f"{prepend}-{year}-{month}-Wired.docx")
    createreport.makeReport(txtfile, dict_wlan0, prepend+"wlan0.png", f"{prepend}-{year}-{month}-WiFi.docx")
    ####DELETE INTERMEDIATE FILES###
    for file_name in os.listdir(directory):
        if file_name.endswith('.png'):
            os.remove(file_name)

if __name__ == "__main__":  
    directory = os.getcwd()  
###SETTING UP ARGPARSE###
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=str)
    parser.add_argument("month", type=str)
    parser.add_argument("txtfile", type=str)
    parser.add_argument("url", type=str)
    args = parser.parse_args()
    year = args.year
    month = str(int(args.month))
    txtfile = args.txtfile
    url = args.url
    ###IF DOCX ALREADY EXISTS###
    for file_name in os.listdir(directory):
        if file_name == f"{year}-{month}-Wired.docx":
            print("will overwrite existing docx files")
    ###MONTH NUM : DAY NUM DICT###
    month_days = {
        1: 31,  # January
        2: 28,  # February
        3: 31,  # March
        4: 30,  # April
        5: 31,  # May
        6: 30,  # June
        7: 31,  # July
        8: 31,  # August
        9: 30,  # September
        10: 31,  # October
        11: 30,  # November
        12: 31   # December
    }
    ###FETCHING###
    data = fetch(url)
    ###FILTER AND SORT###
    fsdata = filterSort(data)
    ###FILTER FOR WIRED AND WIFI###
    filtered_eth0 = filterit(fsdata, month, year)
    if len(filtered_eth0)==0:
        print("the year / month requested has no data after filtering")
        exit(1)
    filtered_wlan0 = filterit(fsdata, month, year, "wlan0")
    if len(filtered_wlan0)==0:
        print("the year / month requested has no data after filtering")
        exit(1)

    ##MAKE DATA DICTIONARIES FOR WIRED AND WIFI###
    dict_eth0 = analyze(filtered_eth0, "eth0")
    dict_wlan0 = analyze(filtered_wlan0, "wlan0")
    ##MAKE PLOTS###
    plotdata.createPlot(plotdata.dailyAvg(filtered_eth0, month_days[int(month)]), "eth0.png")
    plotdata.createPlot(plotdata.dailyAvg(filtered_wlan0, month_days[int(month)]), "wlan0.png")
    ##MAKE REPORTS###
    createreport.makeReport(txtfile, dict_eth0, "eth0.png", f"{year}-{month}-Wired.docx")
    createreport.makeReport(txtfile, dict_wlan0, "wlan0.png", f"{year}-{month}-WiFi.docx")
    ###DELETE INTERMEDIATE FILES###
    for file_name in os.listdir(directory):
        if file_name.endswith('.png'):
            os.remove(file_name)

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
#print("\n############################################\n")
#print(dict)
#output(dict)
