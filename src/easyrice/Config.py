#!/usr/bin/python

import os

def getconfig(filename):
	if filename == None:
		filename = os.environ['HOME'] + "/.config/easyrice/config"
	print(filename)
	file = open(filename, "r")
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
	if "size" not in toReturn:
		toReturn["size"] = 15
	return toReturn



def getcommands(filename):
	if filename == None:
		filename = os.environ['HOME'] + "/.config/easyrice/commands"
	file = open(filename, "r")
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
			if "height" not in curr:
				curr["height"] = 0
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
