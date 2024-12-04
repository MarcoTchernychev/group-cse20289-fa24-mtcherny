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
def filter(json, date, time, field):
    #first filter by field
    []
