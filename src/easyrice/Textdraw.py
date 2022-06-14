#!/usr/bin/python

# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
#KEEP TRACK OF LINK

from PIL import ImageFont, Image, ImageDraw
import os, sys, subprocess
import easyrice.Textvalues


class TextCreation:
    def __init__(self, draw, font,bold,cursive):
        self.draw = draw

        #INIT FONTS AND SET FIRST VALUE
        self.fonts = {}
        self.fonts["font"] = font
        self.fonts["bold"] = bold
        self.fonts["cursive"] = cursive
        self.font = self.fonts["font"]
        self.size = font.getsize("a")
        #THIS IS ADDED AS A SMALL MARGIN BETWEEN THE LINES
        self.size = (self.size[0], self.size[1] + 1)
        print(self.size)
        self.strikethrough = False
        self.underline = False

        #COLOR INIT
        self.color = Textvalues.black()
        self.foreground = Textvalues.white()

        #REST INIT
        self.pos = (0,0)
        self.maxpos = (0,0)
        self.savedpos = self.pos
        self.buffer = ""


    def commandToText(self, command, x, y, width, heigth):
        self.maxpos = (width/self.size[0], heigth/self.size[1])
        print("MAX", self.maxpos)
        command = command.strip("\n").split(" ")
        result = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode("utf-8")
        print(result)
        self._writetext(result, x, y)

    def _writetext(self, text, x, y):
        self.relative = (x,y)
        self.pos = (0,0)
        self.savedpos = self.pos
        i = 0
        while(i < len(text)):
            if (text[i] == '\x1B'):
                self._flush()
                i = self._handleescape(text, i)
                continue
            if (text[i] == '\n'):
                self._newline()
                i += 1
                continue
            self._addchar(text[i])
            i += 1
        self._flush()
        self.foreground = Textvalues.white()
        self.color = Textvalues.black()
        self.underline = False
        self.strikethrough = False

    def _newline(self):
        self._flush()
        print("Pre")
        print(self.pos)
        self.pos = (0, self.pos[1] + 1)
        print("Post")
        print(self.pos)

    def _addchar(self, char):
        self.buffer += char

    def _flush(self):
        pos = (self.pos[0]*self.size[0] +self.relative[0], self.pos[1]*self.size[1] + self.relative[1])
        if self.color is not Textvalues.black():
            points = ((pos[0], pos[1]), (pos[0] + self.size[0]*len(self.buffer), self.size[1] + pos[1]))
            self.draw.rectangle(points, fill=self.color, outline=self.color)

        self.draw.text( pos, self.buffer, font=self.font, fill=self.foreground)
        if self.underline == True:
            self.draw.line(((pos[0], pos[1] + self.size[1]),(pos[0] + self.size[0]*len(self.buffer), self.size[1] + pos[1])))
        if self.strikethrough == True:
            self.draw.line(((pos[0],pos[1]+self.size[1]/2),(pos[0] + self.size[0]*len(self.buffer),pos[1]+ self.size[1]/2)))
        self.pos = (self.pos[0] + len(self.buffer), self.pos[1])
        self.buffer = ""

#Handle escape sequences
    def _handleescape(self, text, i):
        i += 1
        if (text[i] != "["):
            return i
        i += 1
        if not text[i].isnumeric():
            if (text[i] == "s"):
                print("Save: " , self.pos)
                self.savedpos = self.pos
                return i + 1
            if (text[i] == "u"):
                print("Restore: " , self.pos)
                self.pos = self.savedpos
                return i + 1
            i += 1
            while True:
                if (text[i] == "h" or text[i] == "l"):
                    return i + 1
                i += 1
        numbers = []
        number = "" + text[i]
        i += 1
        done = False
        while not done:
            while text[i].isnumeric():
                number += text[i]
                i += 1
            numbers.append(int(number))
            number = ""
            if text[i] != ';':
                done = True
            else:
                i += 1
        print("Number: "  + str(number) + " Position: " + str(self.pos[1]) + " Letter " + text[i])
        if text[i] == 'A':
            self.pos = (self.pos[0] , self.pos[1] - numbers[0])
        elif text[i] == 'B':
            self.pos = (self.pos[0], self.pos[1] + numbers[0])
        elif text[i] == 'C':
            self.pos = (self.pos[0] + numbers[0], self.pos[1])
        elif text[i] == 'D':
            self.pos = (self.pos[0] - numbers[0], self.pos[1])
        elif text[i] == 'E':
            self.pos = (0, self.pos[1] + numbers[0] + 1)
        elif text[i] == 'F':
            self.pos = (0, self.pos[1] + numbers[0] -1)
        elif text[i] == 'G':
            self.pos= (self.pos[0],numbers[0])
        elif text[i] == 'm':
            self._handlem(numbers)
        else:
            #KEEP THIS PRINT
            print("UNKNOWN ESCAPE SEQUENCE CLOSE TO POSITION " + text[i])
            return i
        self._checkposition()
        return i + 1

    def _handlem(self,numbers):
        if numbers[0] == 38 or numbers[0] == 48:
            if numbers[1] == 5:
                if numbers[0] == 38:
                    self.foreground = Textvalues.getbytecolor(numbers[2])
                else:
                    self.color = Textvalues.getbytecolor(numbers[2])
                return

        for number in numbers:
            if number == 0:
                self.foreground = Textvalues.reset()
                self.color = Textvalues.black()
                self.underline = False
                self.strikethrough = False
                continue
            if number == 1:
                self.font = self.fonts["bold"]
                continue
            elif number < 10:
                if number == 1:
                    self.font = self.fonts["bold"]
                    continue
                elif number == 2:
                    self.foreground = (int(self.foreground[0]/2), int(self.foreground[1]/2), int(self.foreground[2]/2), 255)
                    continue
                elif number == 3:
                    self.font = self.fonts["cursive"]
                    continue
                elif number == 4:
                    self.underline = True
                    continue
                elif number == 7:
                    temp = self.foreground
                    self.foreground = self.color
                    self.color = temp
                    continue
                elif number == 8:
                    self.foreground = self.color
                    continue
                elif number == 9:
                    self.strikethrough = True
                    continue
                #KEEP THIS PRINT
                print("5m not supported, an image can't blink!!!!!")
                continue
            elif number < 40:
                self.foreground = Textvalues.getcolor(number % 10)
            else:
                self.color = Textvalues.getcolor(number % 10)

    def _checkposition(self):
        if self.pos[0] > self.maxpos[0]:
            self.pos = (self.maxpos[0], self.pos[1])
        if self.pos[1] > self.maxpos[1]:
            self.pos = (self.pos[0], self.maxpos[1])
        if self.pos[1] < 0:
            print("Correction")
            self.pos = (self.pos[0], 0)
        if self.pos[0] < 0:
            print("Correction")
            self.pos = (0, self.pos[1])


