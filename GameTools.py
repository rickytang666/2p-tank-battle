# Importing packages

from tkinter import*
from math import*
from time import*
from random import*


# Initializing the screen with constants

WIDTH = 1200
HEIGHT = 1000
BACKGROUND_COL = "white"

myInterface = Tk()
screen = Canvas(myInterface, width = WIDTH, height = HEIGHT, background = BACKGROUND_COL)
screen.pack()


# General drawing/calculating methods

def ConvertAngle(angle):
    return (450 - angle) % 360


def draw_rotated_rectangle(centerX, centerY, length, width, angle, col):
    
    # Calculate the corners of the rectangle
    corners = []

    for dx, dy in [(-length/2, -width/2), (-length/2, width/2), (length/2, width/2), (length/2, -width/2)]:

        dx_rot = dx * cos(radians(angle)) + dy * sin(radians(angle))
        dy_rot = -dx * sin(radians(angle)) + dy * cos(radians(angle))  # Subtract instead of add
        corners.append((centerX + dx_rot, centerY + dy_rot))
    
    return screen.create_polygon(*corners, fill=col, outline=col)


############################################3


# Classes

class Tank:
    
    def __init__ (self, id, x, y, angle):
        
        # Initialize the properties

        self.id = id if id == 1 else 2
        self.name = "Player" + str(self.id)
        self.color1 = "blue4" if self.id == 1 else "forest green"
        self.color2 = "sky blue" if self.id == 1 else "green2"
        self.length = 40
        self.width = 30
        self.speed = 20
        self.x = x
        self.y = y
        self.angle = angle

        # Initialize the drawings
        self.body = 0
        self.platform = 0
        self.cannon = 0
        
        
    def draw(self):
        
        self.body = draw_rotated_rectangle(self.x, self.y, self.length, self.width, self.angle, self.color2)
        self.platform = draw_rotated_rectangle(self.x, self.y, self.length * 0.8, self.width * 0.8, self.angle, self.color1)

        endX = self.x + self.length * 0.8 * cos(radians(self.angle))
        endY = self.y - self.length * 0.8 * sin(radians(self.angle))  # Subtract instead of add

        self.cannon = screen.create_line(self.x, self.y, endX, endY, fill=self.color1, width=self.width * 0.3)

    def go(self):
        # Move the tank forward in the direction it's pointing
        self.x += self.speed * cos(radians(self.angle))
        self.y -= self.speed * sin(radians(self.angle))  # Subtract instead of add

    def go_back(self):
        # Move the tank backward in the direction it's pointing
        self.x -= self.speed * cos(radians(self.angle))
        self.y += self.speed * sin(radians(self.angle))  # Add instead of subtract

    def delete(self):

        screen.delete(self.body, self.platform, self.cannon)


#####################################################################################################

def setInitialValues():

    global tank1, tank2 # objects
    global FPS

    tank1 = Tank(1, 50, 50, 0)
    tank2 = Tank(2, WIDTH - 50, HEIGHT - 50, 180)
    FPS = 144


def keyDownHandler(event):

    if event.keysym == "a":

        tank1.angle += 5

    elif event.keysym == "d":

        tank1.angle -= 5

    elif event.keysym == "w":

        tank1.go()

    elif event.keysym == "s":
        
        tank1.go_back()


    if event.keysym == "Left":

        tank2.angle += 5

    elif event.keysym == "Right":

        tank2.angle -= 5

    elif event.keysym == "Up":

        tank2.go()

    elif event.keysym == "Down":

        tank2.go_back()


def runGame():

    setInitialValues()

    for f in range(100000):

        tank1.draw()
        tank2.draw()

        # update/sleep/delete
        screen.update()
        sleep(1/FPS)
        tank1.delete()
        tank2.delete()

# Bindings
screen.bind( "<Key>", keyDownHandler)

screen.focus_set()  # Set focus to the canvas

runGame()

myInterface.mainloop()