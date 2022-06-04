#!/usr/bin/python

import Config
import sys
import Add
from PIL import Image,  ImageEnhance, ImageFilter, ImageFont, ImageDraw
import Textdraw
import argparse
from Getimage import get_image

parser = argparse.ArgumentParser(description="Easy rice");
parser.add_argument("-con","--config", dest="config", type=str, help="Path to configurationfile")
parser.add_argument("-com", "--commands", dest="command", type=str, help="Path to commandfile")
parser.add_argument("-d", "--dest", required=True, dest="dest", type=str, help="Path to save file")
parser.add_argument("-s", "-src", required=True, dest="src", type=str, help="Path to image")
parser.add_argument("-b", "--black", nargs="?",const="black", default="True", dest="black", type=bool, help="Have a black frame instead of an image")
args = parser.parse_args()

commands = Config.getcommands(args.command)
config = Config.getconfig(args.config)

if (len(sys.argv) < 3):
	print("Too few commands it needs to be NAME + <filepath>")
	sys.exit(-1)
Image.open(args.src, "r")
img = get_image(args)
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
font = ImageFont.truetype(config["font"].strip("\n"), 15)
#bold = ImageFont.truetype(config["bold"].strip("\n"))
#cursive = ImageFont.truetype(config["cursive"].strip("\n"))
bold = font
cursive = bold
text = Textdraw.TextCreation(draw, font, bold,cursive)
for c in commands:
	#TODO Maybe? Fix so there are flexible margins.
	text.commandToText(c["command"], c["x"] + 6, c["y"] + 6, c["width"], c["heigth"])
img.save(args.dest, "PNG")

