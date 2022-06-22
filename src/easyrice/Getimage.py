from PIL import Image
from easyrice.Config import getcommands

def get_image(args):
    
    if args.black == True:
        commands = getcommands(args.command)
        x = 0
        y = 0
        for c in commands:
            if int(c["x"]) + int(c["width"]) > x:
                x = int(c["x"]) + int(c["width"])
            if int(c["y"]) + int(c["heigth"]) > y:
                y = int(c["y"]) + int(c["heigth"])
        return Image.new("RGB", (x,y), (0,0,0))

    return Image.open(args.src, "r")

