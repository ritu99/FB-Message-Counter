import fb_parser as fb_parser
import overall_grapher as overall_grapher
import grapher as grapher
import sys
from tkinter import *
import tkinter.filedialog
import matplotlib


def graph():
    curr_in = ''

    while True:
        print("\nExtract data from which person?\nType 'Overall' to recieve an overall graph.\nType 'exit' to exit")
        curr_in = input()
        if curr_in == 'exit':
            break
        if curr_in == 'Overall':
            overall_grapher.overall_graph()
        else:
            try:
                grapher.graph_person(curr_in)
            except IOError:
                print("No such person found!")
    sys.exit()

print("""*******************************************************************************
          |                   |                  |                     |
 _________|________________.=\"\"_;=.______________|_____________________|_______
|                   |  ,-\"_,=\"\"     `\"=.|                  |
|___________________|__\"=._o`\"-._        `\"=.______________|___________________
          |                `\"=._o`\"=._      _`\"=._                     |
 _________|_____________________:=._o \"=._.\"_.-=\"'\"=.__________________|_______
|                   |    __.--\" , ; `\"=._o.\" ,-\"\"\"-._ \".   |
|___________________|_._\"  ,. .` ` `` ,  `\"-._\"-._   \". '__|___________________
          |           |o`\"=._` , \"` `; .\". ,  \"-._\"-._; ;              |
 _________|___________| ;`-.o`\"=._; .\" ` '`.\"\` . \"-._ /_______________|_______
|                   | |o;    `\"-.o`\"=._``  '` \" ,__.--o;   |
|___________________|_| ;     (#) `-.o `\"=.`_.--\"_o.-; ;___|___________________
____/______/______/___|o;._    \"      `\".o|o_.--\"    ;o;____/______/______/____
/______/______/______/_\"=._o--._        ; | ;        ; ;/______/______/______/_
____/______/______/______/__\"=._o--._   ;o|o;     _._;o;____/______/______/____
/______/______/______/______/____\"=._o._; | ;_.--\"o.--\"_/______/______/______/_
____/______/______/______/______/_____\"=.o|o_.--\"\"___/______/______/______/____
/______/______/______/______/______/______/______/______/______/______/[4u Ira]
*******************************************************************************""")
if fb_parser.has_extracted() == False:
    print("What's your name on Facebook?")
    try:
        fb_parser.extract_data(input())
        graph()
    except IOError:
        print("Extract the downloaded archive and put it in the same folder as this exe")
else:
    graph()
