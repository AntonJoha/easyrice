import Config
import sys
import Add
from PIL import Image,  ImageEnhance, ImageFilter, ImageFont, ImageDraw
import Textdraw
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
        if int(c["y"]) + int(c["heigth"]) > y:
            y = int(c["y"]) + int(c["width"])
    return Image.new("RGB", (x,y), (0,0,0))

def make_image(config, commands, out , inFile=None , blend =0.8, fontSize=10):
    commands = Config.getcommands(commands)
    config = Config.getconfig(config)
    
    img = get_image(inFile, commands)

    copy = img.copy()
    draw = ImageDraw.Draw(copy)


    for c in commands:
        Add.addrectangle(draw, int(c["x"]), int(c["x"]) + int(c["width"]),
                int(c["y"]), int(c["y"]) + int(c["height"]))

    img = Image.blend(img,copy, blend)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(config["font"].strip("\n"), fontSize)
    bold = ImageFont.truetype(config["bold"].strip("\n"), fontSize)
    cursive = ImageFont.truetype(config["cursive"].strip("\n"), fontSize)

    text = Textdraw.TextCreation(draw, font, bold, cursive)

    for c in commands:
        text.commandToText(c["command"], int(c["x"]) + 6, int(c["y"]) + 6, int(c["width"]), int(c["heigth"]))
    img.save(out, "PNG")
    

