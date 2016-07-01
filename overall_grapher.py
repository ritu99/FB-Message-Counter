import datetime
import numpy as np
import csv
import matplotlib.pyplot as plot
from math import ceil
import os

def overall_graph():
    legend = []

    LOADING = 0
    for file in os.listdir("extracted_data/"):
        if file.endswith(".csv"):
            LOADING += 1
            print('loading' + '.' * ((LOADING//10)%4) +"     ",end='\r')
            messageTable = []
            with open('extracted_data/'+file,'r', encoding="utf8") as currcsv:
                tab = csv.reader(currcsv)
                for row in tab:
                    index = 0
                    messageDate = ""
                    for col in row:
                        if index == 2 or index == 3:
                            messageDate  = messageDate + col + " "
                        index += 1
                    if len(messageDate) > 15:
                        messageTable.append(datetime.datetime.strptime(messageDate[:-5], "%B %d %Y %I:%M%p"))
            messageTable.append(datetime.datetime.now())
            messageTable.sort()
            if len(messageTable) > 4000:
                plot.plot(messageTable,[i for i in range(len(messageTable))],label="%s (%d)" % (file[:-4],len(messageTable)),linewidth=3)



    leg = plot.legend(bbox_to_anchor=(0, 1), loc='upper left', ncol=1)

    for legobj in leg.legendHandles:
        legobj.set_linewidth(3.0)

    print()
    plot.show()
