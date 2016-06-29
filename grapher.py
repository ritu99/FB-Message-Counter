import datetime
import numpy as np
import csv
import matplotlib.pyplot as plot
import sys
from math import ceil


person = sys.argv[0]

messageTable = []
dailyTable = []
timeTable = []
countTable = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']

with open('extracted_data/%s.csv' % person,'r', encoding="utf8") as currcsv:
    tab = csv.reader(currcsv)
    for row in tab:
        index = 0
        messageDate = ""
        for col in row:
            if index == 2 or index == 3:
                messageDate  = messageDate + col + " "
            if index == 1:
                dailyTable.append(col)
            if index == 3:
                timeTable.append(datetime.datetime.strptime(col[:-4], "%I:%M%p"))
            index += 1
        if len(messageDate) > 15:
            messageTable.append(datetime.datetime.strptime(messageDate[:-5], "%B %d %Y %I:%M%p"))

messageTable.sort()
timeTable.sort()

fig, dataPlots = plot.subplots(2,2)

dataPlots[0,0].hist(messageTable, bins = ceil((messageTable[len(messageTable)-1]-messageTable[0]).days)/7)
dataPlots[0,0].set_title('Number of messages per week')

dataPlots[0,1].bar([0,1,2,3,4,5,6],[dailyTable.count(countTable[i-1]) for i in range(len(countTable))], align='center', tick_label = countTable)

dataPlots[0,1].set_title('Number of messages sent on days of the week')

dataPlots[1,0].hist(timeTable, bins = 48)
dataPlots[1,0].set_title('Number of messages sent at times of the day')

dataPlots[1,1].plot(messageTable,[i for i in range(len(messageTable))])
dataPlots[1,1].set_title('Total number of messages sent')


plot.show()
