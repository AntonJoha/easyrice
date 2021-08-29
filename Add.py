#!/usr/bin/python

import os, sys, subprocess
from PIL import Image, ImageEnhance, ImageFilter, ImageFont, ImageDraw

def addtext(draw, command, pos,font):
	command = command.strip('\n').split(" ")
	result = subprocess.run(command, stdout=subprocess.PIPE)
	output = result.stdout.decode('utf-8')
	draw.text(pos, output,font=font, fill=(0,255,255,255))
	print("Added: " + output)

def addrectangle(draw,x0,x1,y0,y1, color=(0,0,0,255)):
	draw.rounded_rectangle([(x0,y0), (x1,y1)], radius=10, fill=color, width=1)