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
    
if fb_parser.has_extracted() == False:
    print("What's your name on Facebook?")
    try:
        fb_parser.extract_data(input())
        graph()
    except IOError:
        print("Extract the downloaded archive and put it in the same folder as this exe")
else:
    graph()
