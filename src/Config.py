#!/usr/bin/python

import os

def getconfig():
	file = open(os.environ['HOME'] + "/.config/easyrice/config")
	toReturn = {}
	for line in file:
		if line.count("=") != 1:
			continue
		split = line.split("=")
		toReturn[split[0]] = split[1]
	if "font" not in toReturn:
		toReturn["font"] = "/usr/share/fonts/gnu-free/FreeMono.otf"
	if "bold" not in toReturn:
		toReturn["bold"] = "/usr/share/fonts/gnu-free/FreeMonoBold.otf"
	if "cursive" not in toReturn:
		toReturn["cursive"] = "/usr/share/fonts/gnu-free/FreeMonoOblique.otf"
	return toReturn


def getcommands():
	file = open(os.environ['HOME'] + "/.config/easyrice/commands", "r")
	toReturn = []
	curr = {}
	for line in file:
		print(line)
		if line == "[new]\n":
			print("NEW")
			#No reason to draw anything if there's nothing to execute
			if "command" not in curr:
				curr = {}
				continue
			if "x" not in curr:
				curr["x"] = 0
			if "y" not in curr:
				curr["y"] = 0
			if "width" not in curr:
				curr["width"] = 0
			if "heigth" not in curr:
				curr["heigth"] = 0
			toReturn.append( curr)
			curr = {}
		#END IF
		if line.count("=") != 1:
			continue
		pair = line.split('=')
		curr[pair[0]] = pair[1]

	if "command" not in curr:
		return toReturn
	if "x" not in curr:
		curr["x"] = 0
	if "y" not in curr:
		curr["y"] = 0
	if "width" not in curr:
		curr["width"] = 0
	if "heigth" not in curr:
		curr["heigth"] = 0
	toReturn.append( curr)
	return toReturn
