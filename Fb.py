#!/usr/bin/env python
import re
from argparse import ArgumentParser, Namespace
from sys import exit
import os

parser = ArgumentParser(description='Convert Facebook message log to csv files')

parser.add_argument('infile', metavar='INFILE', nargs=1, type=str,
			help='HTML file to convert')

options = parser.parse_args()

def cleanline(line):
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
try:
	for line in open(options.infile[0], 'r', encoding="utf8"):
		oline = line
		line = line.strip()
		if '<div class="thread">' in line:
			if "," in person:
				if not os.path.exists("new/groupchats"):
					os.makedirs("new/groupchats")
				open('new/groupchats/%s.csv' % person, 'a', encoding="utf8").write('\n'.join(cache))
			else:
				open('new/%s.csv' % person, 'a', encoding="utf8").write('\n'.join(cache))
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
