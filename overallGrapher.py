import datetime
import numpy as np
import csv
import matplotlib.pyplot as plot
from math import ceil
import os


legend = []
ritvikCount = 0
othersCount = 0
for file in os.listdir("ritvik/new/"):
    if file.endswith(".csv"):
        messageTable = []
        with open('ritvik/new/'+file,'r', encoding="utf8") as currcsv:
            tab = csv.reader(currcsv)
            for row in tab:
                index = 0
                messageDate = ""
                for col in row:
                    if index == 0:
                        if "Ritvik" in col:
                            ritvikCount+=1
                        else:
                            othersCount+=1
                    if index == 2 or index == 3:
                        messageDate  = messageDate + col + " "
                    index += 1
                if len(messageDate) > 15:
                    messageTable.append(datetime.datetime.strptime(messageDate[:-5], "%B %d %Y %I:%M%p"))
        messageTable.append(datetime.datetime.strptime("June 10 2016 11:59pm","%B %d %Y %I:%M%p"))
        messageTable.sort()
        if len(messageTable) > 4000:
            plot.plot(messageTable,[i for i in range(len(messageTable))],label="%s (%d)" % (file[:-4],len(messageTable)),linewidth=3)


print(ritvikCount)
print(othersCount)
print(ritvikCount+othersCount)
# plot.yscale('log')
# plot.legend(legend)
leg = plot.legend(bbox_to_anchor=(0, 1), loc='upper left', ncol=1)

for legobj in leg.legendHandles:
    legobj.set_linewidth(3.0)

plot.show()
