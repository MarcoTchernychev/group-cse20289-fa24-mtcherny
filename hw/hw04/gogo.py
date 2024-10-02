#Marco Tchernychev
#mtcherny@gmail.com
import argparse
import yaml
import json
from functools import reduce
import checktests.py

#INPUT: a YAMLfile name as str
#OUTPUT: a dictionary of tasks where each task has an identifier, URL, year, month, filename for starting text, and identifier placed at start of name for any output file in the task
#PURPOSE: returns a dict, or None if the file can't load or has missing fields 
def parseYAML(YAMLfile):
    try: #make sure file exists
        with open(YAMLfile, 'r') as file:
            ogYAMLdict = yaml.safe_load(file)["tasks"] #get rid of redundant task key
            YAMLdict = reduce(lambda x,y:{**x,**y}, ogYAMLdict) #combine the dicts in the list into one (** unpacks key vals so were not just making nested dicts)
    except: #if not exists return None
        return None
    for val in YAMLdict.values(): #loop over the dictionaries that are the values
        try: #check to see that you can acces all keys
            if not (val["URL"]!="" and type(val["Year"])==int and type(val["Month"])==int and val["StartText"]!="" and val["Prepend"]!=""): #check to see YAML dict has invalid entries
                return None
        except: #if you can't access all keys, return none
            return None
    return YAMLdict #if you made it past all checks return the dict


#PARSING ARGS
parser = argparse.ArgumentParser()
parser.add_argument("YAMLfile", type=str)
args = parser.parse_args()
YAMLfile = args.YAMLfile

#TESTING
print(json.dumps(parseYAML(YAMLfile), indent=4))