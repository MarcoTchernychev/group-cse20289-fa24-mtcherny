#Marco Tchernychev
#mtcherny@gmail.com
import argparse
import yaml
import json
from functools import reduce
import checktests
from spire.doc import *
from spire.doc.common import *
import os
import concurrent.futures
import traceback

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
#INPUT: dictionary of one task and the task
#OUTPUT: returns nothing but outputs a pdf that has the same content as the word document from hw3, also, print whne each task is done and when all tasks are done
#PURPOSE: print the pdf in a concise way
def dataToPDF(taskDict, task):
    try:
        checktests.doItAll(taskDict["Year"], taskDict["Month"], taskDict["StartText"], taskDict["URL"], taskDict["Prepend"], task) #create docx
        document1 = Document() #create first pdf doc
        document1.LoadFromFile(f"{taskDict['Prepend']}-{taskDict['Year']}-{taskDict['Month']}-Wired.docx")
        document1.SaveToFile(f"{taskDict['Prepend']}-{taskDict['Year']}-{taskDict['Month']}-Wired.pdf", FileFormat.PDF)
        document1.Close()
        document2 = Document() #create second pdf doc
        document2.LoadFromFile(f"{taskDict['Prepend']}-{taskDict['Year']}-{taskDict['Month']}-WiFi.docx")
        document2.SaveToFile(f"{taskDict['Prepend']}-{taskDict['Year']}-{taskDict['Month']}-WiFi.pdf", FileFormat.PDF)
        document2.Close()
        os.remove(f"{taskDict['Prepend']}-{taskDict['Year']}-{taskDict['Month']}-Wired.docx") #delete docx files
        os.remove(f"{taskDict['Prepend']}-{taskDict['Year']}-{taskDict['Month']}-WiFi.docx") #delete docx files
        print(f"Task {task} Done!")
    except Exception as E:
        print("exception", E)
        tb = traceback.format_exc()
        print("Traceback info:")
        print(tb)
        exit(1)

#def allGogo()

#PARSING ARGS
parser = argparse.ArgumentParser()
parser.add_argument("YAMLfile", type=str, help="Path to the YAML file")
parser.add_argument("--multi", type=int, help="Number of processors to use")
args = parser.parse_args()
YAMLfile = args.YAMLfile
processors = args.multi
#PARSE THE YAML
tasks_dict = parseYAML(YAMLfile)
if not tasks_dict:
    ("print no YAML")
    exit(1)
#PARALLEL CASE
if args.multi:
    with concurrent.futures.ProcessPoolExecutor(max_workers=processors) as executor:
        executor.map(dataToPDF, [tup[1] for tup in list(tasks_dict.items())], [tup[0] for tup in list(tasks_dict.items())])
    print(f"Completed {len(tasks_dict)} task(s)!")
#NOT PARALLEL CASE
else:
    for task in tasks_dict:
        dataToPDF(tasks_dict[task], task)
    print(f"Completed {len(tasks_dict)} task(s)!")

#TESTING
#print(json.dumps(tasks_dict, indent=4))
#for task in tasks_dict:
#    dataToPDF(tasks_dict[task], task)
#print(f"Completed {len(tasks_dict)} task(s)!")