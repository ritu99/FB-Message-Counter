#!/usr/bin/env python
import re
from argparse import ArgumentParser, Namespace
from sys import exit
import os

parser = ArgumentParser(description='Convert Facebook message log to csv files')

parser.add_argument('name', metavar='NAME', nargs=1, type=str,
			help='HTML file to convert')

options = parser.parse_args()

def cleanline(line):
	# line = line.replace(",","[[COMMA]]")
	for trash in ('<div class="message_header">', '<span class="user">', '</.*?>'):
		line = re.sub(trash, '', line)
	for commafy in ('<span class="meta">', '<p>'):
		line = re.sub(commafy, ',', line)
	return line

cache = []
linebuff = ''
person = ''
buffering = True
linenumber = 1

name = options.name

fb_id = None

for name in os.listdir():
	if "facebook-" in name:
		fb_id = name;

if os.path.isdir("extracted_data") == False:
	os.mkdir("extracted_data/")


if os.path.exists(fb_id+"/html/settings.txt") and 'already-divd!' in open(fb_id+"/html/settings.txt",'r', encoding="utf8").read():
	print("no need to do this stuff")
else:
	f1 = open(fb_id+"/html/messages.htm", 'r', encoding="utf8")
	repl = ''
	for line in f1:
	    repl+=line.replace('<div', '\n<div')
	f1.close()
	f2 = open(fb_id+"/html/messages.htm", 'w', encoding="utf8")
	f2.write(repl)
	f2.close()

	open(fb_id+"/html/settings.txt", 'a', encoding="utf8").write("already-divd!")

if os.path.exists(fb_id+"/html/settings.txt") and 'already-extracted!' in open(fb_id+"/html/settings.txt",'r', encoding="utf8").read():
	print("no need to do this stuff")
else:
	try:
		for line in open(fb_id+"/html/messages.htm", 'r', encoding="utf8"):
			oline = line
			line = line.strip()
			if '<div class="thread">' in line:
				if "," in person or "facebook" in person:
					if not os.path.exists("extracted_data/groupchats"):
						os.makedirs("extracted_data/groupchats")
					open('extracted_data/groupchats/%s.csv' % person, 'a', encoding="utf8").write('\n'.join(cache))
				else:
					open('extracted_data/%s.csv' % person, 'a', encoding="utf8").write('\n'.join(cache))
				print ('Finished %s' % person)
				cache = []
				person = line[len(r'<div class="thread">'):].replace(', Ritvik Annam','').replace(", Ronit AkaRitvik Roy","").replace("Ritvik Annam, ","")[:30]
			elif any(line.startswith(s) for s in ('<div class="message">', '<html>', '<div class="nav">', '<div class="contents">', '<div>', '<div class="footer">')):
				pass
			else:
				buffering = '</p>' not in line
				linebuff += cleanline(line)
			if not buffering:
				linebuff = linebuff.split(',')
				year, time = linebuff[3].split('at')
				linebuff[2] += '%s' % year
				linebuff[3] = time.strip()
				linebuff = ','.join(map(str.strip, linebuff))
				cache.append(linebuff)
				linebuff = ''
				buffering = True
			linenumber += 1
	finally:
		print ('Finished with line number %d' % linenumber)
		open(fb_id+"/html/settings.txt", 'a', encoding="utf8").write("\nalready-extracted!")
