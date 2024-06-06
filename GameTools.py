# Importing packages

from tkinter import*
from math import*
from time import*
from random import*


# Initializing the screen with constants

WIDTH = 400
HEIGHT = 300
BACKGROUND_COL = "white"

myInterface = Tk()
screen = Canvas(myInterface, width = WIDTH, height = HEIGHT, background = BACKGROUND_COL)


# General drawing methods

def draw_rectangle(centerX, centerY, length, width, col):
    
    x1, x2 = centerX - length/2, centerX + length/2
    y1, y2 = centerY - width/2, centerY + width/2
    
    return screen.create_rectangle(x1,y1,x2,y2,fill=col,outline=col)


############################################3


# Classes

class Tank:
    
    def __init__ (self, id, x, y, angle):
        
        self.id = id
        self.name = "Player" + str(id)
        self.color1 = "blue4" if self.id == 1 else "forest green"
        self.color2 = "sky blue" if self.id == 1 else "green2"
        self.length = 40
        self.width = 30
        self.x = x
        self.y = y
        self.angle = angle
        
        
    def draw(self):
        
        self.body = draw_rectangle(self.x,self.y,self.length,self.width,self.color2)
        self.platform = draw_rectangle(self.x,self.y,self.length*0.8,self.width*0.8,self.color1)
        
        
        
        
        
