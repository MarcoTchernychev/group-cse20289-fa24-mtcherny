#Marco Tchernycheb
#mtcherny@nd.edu
import argparse
import requests
import json

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

parser = argparse.ArgumentParser()
parser.add_argument("url", type=str)
args = parser.parse_args()
url = args.url
data = fetch(url)
#filterSort(data)

###TESTS###
#print(type(data)) #list
#print(data) #list
#data_string = json.dumps(data, indent = 4)
#print(data_string) #nice looking string