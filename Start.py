#!/usr/bin/python

import Config
import sys
import Add
from PIL import Image,  ImageEnhance, ImageFilter, ImageFont, ImageDraw
import Textdraw

commands = Config.getcommands()
config = Config.getconfig()

if (len(sys.argv) < 3):
	print("Too few commands it needs to be NAME + <filepath>")
	sys.exit(-1)

img = Image.open(sys.argv[1], "r")
copy = img.copy()

draw = ImageDraw.Draw(copy)
#TODO FIX SO THIS ISN't HARDCODED

for c in commands:
	c["x"] = int(c["x"])
	c["width"] = int(c["width"])
	c["y"] = int(c["y"])
	c["heigth"] = int(c["heigth"])
	Add.addrectangle(draw, c["x"], c["x"] + c["width"], c["y"], c["y"] + c["heigth"])
img = Image.blend(img, copy, 0.8)
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(config["font"].strip("\n"))
bold = ImageFont.truetype(config["bold"].strip("\n"))
cursive = ImageFont.truetype(config["cursive"].strip("\n"))
text = Textdraw.TextCreation(draw, font, bold,cursive)
for c in commands:
	#TODO Maybe? Fix so there are flexible margins.
	text.commandToText(c["command"], c["x"] + 6, c["y"] + 6, c["width"], c["heigth"])
img.save(sys.argv[2], "PNG")

