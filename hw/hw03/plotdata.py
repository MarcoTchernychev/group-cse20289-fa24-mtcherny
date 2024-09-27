#Marco Tchernychev
#mtcherny@nd.edu
import matplotlib.pyplot as plt
import json
import argparse
import statistics

#INPUT: filepath a string
#OUTPUT: JSON file as list
#PURPOSE load in a file
def getfile(filepath):
    with open(filepath, "r") as file:
        data = json.load(file)
        return data
#INPUT: JSON file as a list
#OUTPUT: dict with the day of the month and its average throughput
#PURPOSE: find the daily average for each day in the month before we plot it
def dailyAvg(data, days):
    dict = {}
    for day in range(1, int(days)+1):
        dict[day] = round(statistics.mean([entry["tput_mbps"] for entry in list(filter(lambda x: int(x["timestamp"][8:10])==day, data))]),2)
    for day in range(1, int(days)+1): #checks to see if there was day that didn't have any data
        if day not in dict:
            dict[day] = 0
    return dict
#INPUT: dict with days as keys and average tput as value, name of the output file
#OUTPUT: none, just makes a figure and outputs it to your directory
#PURPOSE: take in a dict and plot average daily tput for a month by day
def createPlot(dict, outputfile):
    plt.bar([key for key in dict],[dict[key] for key in dict])
    plt.xlabel('Day')
    plt.ylabel('Average Throughput (Mb/s)')
    plt.savefig(outputfile)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", type=str)
    parser.add_argument("days", type=str)
    parser.add_argument("outputfile", type=str)
    args = parser.parse_args()
    filepath = args.filepath
    days = args.days
    outputfile = args.outputfile

    data = json.loads(open(args.filepath).read())
    daily_avg_dict = dailyAvg(data, days)
    createPlot(daily_avg_dict, outputfile)
    #data = getfile(filepath)
    #print(type(data))
    #print(json.dumps(data, indent=4))
    #for key in daily_avg_dict:
    #    print(f"{key}: {daily_avg_dict[key]}")
    

