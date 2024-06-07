from tkinter import *
from math import *
from time import *


# Initializing the screen with constants

WIDTH = 700
HEIGHT = 500
BACKGROUND_COL = "white"

myInterface = Tk()
screen = Canvas(myInterface, width=WIDTH, height=HEIGHT, background=BACKGROUND_COL)
screen.pack()


# General drawing/calculating methods

def ConvertAngle(angle):
    return (450 - angle) % 360


def draw_rotated_rectangle(centerX, centerY, length, width, angle, col):
    # Calculate the corners of the rectangle
    corners = []

    for dx, dy in [(-length / 2, -width / 2), (-length / 2, width / 2), (length / 2, width / 2), (length / 2, -width / 2)]:
        dx_rot = dx * cos(radians(angle)) + dy * sin(radians(angle))
        dy_rot = -dx * sin(radians(angle)) + dy * cos(radians(angle))  # Subtract instead of add
        corners.append((centerX + dx_rot, centerY + dy_rot))

    return screen.create_polygon(*corners, fill=col, outline=col)


############################################3


# Classes

class Tank:

    def __init__(self, id, x, y, angle, enemy=None):
        # Initialize the properties
        self.id = id
        self.name = "Player" if self.id == 1 else "Enemy"
        self.color1 = "blue4" if self.id == 1 else "forest green"
        self.color2 = "sky blue" if self.id == 1 else "green2"
        self.length = 45
        self.width = 40
        self.speed = 2
        self.x = x
        self.y = y
        self.angle = angle
        self.shield_radius = 35
        self.enemy = enemy

        # Initialize the drawings
        self.body = 0
        self.platform = 0
        self.cannon = 0
        self.shield = 0

    def draw(self):
        self.body = draw_rotated_rectangle(self.x, self.y, self.length, self.width, self.angle, self.color2)
        self.platform = draw_rotated_rectangle(self.x, self.y, self.length * 0.8, self.width * 0.8, self.angle, self.color1)

        endX = self.x + 35 * cos(radians(self.angle))
        endY = self.y - 35 * sin(radians(self.angle))  # Subtract instead of add

        self.cannon = screen.create_line(self.x, self.y, endX, endY, fill=self.color1, width=10)
        self.shield = screen.create_oval(self.x - self.shield_radius, self.y - self.shield_radius,
                                         self.x + self.shield_radius, self.y + self.shield_radius, outline="gray")

    def go(self):
        # Move the tank forward in the direction it's pointing
        new_x = self.x + self.speed * cos(radians(self.angle))
        new_y = self.y - self.speed * sin(radians(self.angle))  # Subtract instead of add
        if not self.check_collision(new_x, new_y):
            self.x = new_x
            self.y = new_y

    def go_back(self):
        # Move the tank backward in the direction it's pointing
        new_x = self.x - self.speed * cos(radians(self.angle))
        new_y = self.y + self.speed * sin(radians(self.angle))  # Add instead of subtract
        if not self.check_collision(new_x, new_y):
            self.x = new_x
            self.y = new_y

    def check_collision(self, x, y):
        # Check if the tank's circular shield is within the screen boundaries
        if (x - self.shield_radius < 0 or x + self.shield_radius > WIDTH or
                y - self.shield_radius < 0 or y + self.shield_radius > HEIGHT):
            return True

        # Check for collisions with the enemy tank
        if self.enemy != None:
            distance = sqrt((self.enemy.x - x) ** 2 + (self.enemy.y - y) ** 2)
            if distance < self.shield_radius + self.enemy.shield_radius:
                return True

        return False

    def delete(self):
        screen.delete(self.body, self.platform, self.cannon, self.shield)


#####################################################################################################

def setInitialValues():
    global tank1, tank2  # objects
    global FPS

    tank1 = Tank(1, 50, 50, 0)
    tank2 = Tank(2, WIDTH - 50, HEIGHT - 50, 180, tank1)
    tank1.enemy = tank2
    FPS = 144


def keyDownHandler(event):
    keys_pressed[event.keysym] = True


def keyUpHandler(event):
    keys_pressed[event.keysym] = False


def operationsControl():
    if keys_pressed["a"]:
        tank1.angle += 2

    if keys_pressed["d"]:
        tank1.angle -= 2

    if keys_pressed["w"]:
        tank1.go()

    if keys_pressed["s"]:
        tank1.go_back()

    if keys_pressed["Left"]:
        tank2.angle += 2

    if keys_pressed["Right"]:
        tank2.angle -= 2

    if keys_pressed["Up"]:
        tank2.go()

    if keys_pressed["Down"]:
        tank2.go_back()


def runGame():
    setInitialValues()

    for f in range(100000):
        operationsControl()

        tank1.draw()
        tank2.draw()

        # update/sleep/delete
        screen.update()
        sleep(1 / FPS)
        tank1.delete()
        tank2.delete()


# Bindings
screen.bind("<Key>", keyDownHandler)
screen.bind("<KeyRelease>", keyUpHandler)

keys_pressed = {"a": False, "d": False, "w": False, "s": False, "Left": False, "Right": False, "Up": False, "Down": False}

screen.focus_set()  # Set focus to the canvas

runGame()

myInterface.mainloop()
