#!/usr/bin/python

import Config
import sys
import Add
from PIL import Image,  ImageEnhance, ImageFilter, ImageFont, ImageDraw
import Textdraw
import argparse
from Makeimage import make_image


if __name__ == "__main__":
   
    parser = argparse.ArgumentParser(description="Easy rice");
    parser.add_argument("-con","--config", dest="config", type=str, help="Path to configurationfile")
    parser.add_argument("-com", "--commands", dest="command", type=str, help="Path to commandfile")
    parser.add_argument("-d", "--dest", required=True, dest="dest", type=str, help="Path to save file")
    parser.add_argument("-s", "-src", required=True, dest="src", type=str, help="Path to image")
    parser.add_argument("-b", "--black", nargs="?",const="black", default="True", dest="black", type=bool, help="Have a black frame instead of an image")
    args = parser.parse_args()

   
    make_image(args.config, args.command, args.dest, args.src)
