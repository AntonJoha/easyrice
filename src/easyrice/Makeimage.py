from easyrice.Config import getcommands, getconfig
import sys
from easyrice.Add import addrectangle
from PIL import Image,  ImageEnhance, ImageFilter, ImageFont, ImageDraw
from easyrice.Textdraw import TextCreation
import argparse




def get_image(inFile, commands):
    if inFile == None:
        return get_black(commands)
    else:
        return Image.open(inFile, "r")

def get_black(commands):
    x = 0
    y = 0
    for c in commands:
        if int(c["x"]) + int(c["width"]) > x:
            x = int(c["x"]) + int(c["width"])
        if int(c["y"]) + int(c["height"]) > y:
            y = int(c["y"]) + int(c["width"])
    return Image.new("RGB", (x,y), (0,0,0))

def make_image(config, commands, out , inFile=None , blend =0.8):
    commands = getcommands(commands)
    config = getconfig(config)
    
    img = get_image(inFile, commands)

    copy = img.copy()
    draw = ImageDraw.Draw(copy)


    for c in commands:
        addrectangle(draw, int(c["x"]), int(c["x"]) + int(c["width"]),
                int(c["y"]), int(c["y"]) + int(c["height"]))

    img = Image.blend(img,copy, blend)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(config["font"].strip("\n"), int(config["size"]))
    bold = ImageFont.truetype(config["bold"].strip("\n"), int(config["size"]))
    cursive = ImageFont.truetype(config["cursive"].strip("\n"), int(config["size"]))

    text = TextCreation(draw, font, bold, cursive)

    for c in commands:
        text.commandToText(c["command"], int(c["x"]) + 6, int(c["y"]) + 6, int(c["width"]), int(c["height"]))
    img.save(out, "PNG")
    

