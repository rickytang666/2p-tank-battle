from tkinter import *
from math import *
from time import *


# Initializing the screen with constants

WIDTH = 700
HEIGHT = 500
BACKGROUND_COL = "white"
LEFT_WALL, RIGHT_WALL = 80, WIDTH - 80
UP_WALL, DOWN_WALL = 80, HEIGHT - 80

myInterface = Tk()
screen = Canvas(myInterface, width=WIDTH, height=HEIGHT, background=BACKGROUND_COL)
screen.pack()


# General drawing/calculating methods

def ConvertAngle(angle):
    return (450 - angle) % 360


def to_principal(angle):

    return (angle + 180) % 360 - 180



def calculate_distance(x1, y1, x2, y2):
    
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def draw_circle(centerX, centerY, radius, col):
    x1 = centerX - radius
    x2 = centerX + radius
    y1 = centerY - radius
    y2 = centerY + radius
    
    return screen.create_oval(x1, y1, x2, y2, fill = col, outline = col)

def draw_rotated_rectangle(centerX, centerY, length, width, angle, col):
    # Calculate the corners of the rectangle
    corners = []

    for dx, dy in [(-length / 2, -width / 2), (-length / 2, width / 2), (length / 2, width / 2), (length / 2, -width / 2)]:
        dx_rot = dx * cos(radians(angle)) + dy * sin(radians(angle))
        dy_rot = -dx * sin(radians(angle)) + dy * cos(radians(angle))  # Subtract instead of add
        corners.append((centerX + dx_rot, centerY + dy_rot))

    return screen.create_polygon(*corners, fill=col, outline=col)
    
def draw_background():
    
    screen.create_rectangle(LEFT_WALL, UP_WALL, RIGHT_WALL, DOWN_WALL, outline = "black", width = 5)


############################################3


# Classes

class Tank:

    def __init__(self, id, x, y, angle, enemy = None):
        # Initialize the properties
        self.id = id
        self.name = "Player" if self.id == 1 else "Enemy"
        self.color1 = "blue4" if self.id == 1 else "forest green"
        self.color2 = "sky blue" if self.id == 1 else "green2"
        self.length = 45
        self.width = 40
        self.speed = 2
        self.rotate_speed = 1
        self.x = x
        self.y = y
        self.angle = angle
        self.shield_radius = 28
        self.petrol = 20000
        self.shoot_range = 200
        self.enemy = enemy

        # Initialize the drawings
        self.body = 0
        self.platform = 0
        self.cannon = 0
        self.shield = 0

    def draw(self):
        
        # Every time it show up it should consume petrol
        self.petrol -= 1
        
        self.body = draw_rotated_rectangle(self.x, self.y, self.length, self.width, self.angle, self.color2)
        self.platform = draw_rotated_rectangle(self.x, self.y, self.length * 0.6, self.width * 0.6, self.angle, self.color1)

        endX = self.x + 30 * cos(radians(self.angle))
        endY = self.y - 30 * sin(radians(self.angle))  # Subtract instead of add
        
        self.cannon = screen.create_line(self.x, self.y, endX, endY, fill=self.color1, width = 7)
        
        # for debug
        
        self.shield = screen.create_oval(self.x - self.shield_radius, self.y - self.shield_radius,
                                         self.x + self.shield_radius, self.y + self.shield_radius, outline="gray")

    def go(self):
        # Move the tank forward in the direction it's pointing
        new_x = self.x + self.speed * cos(radians(self.angle))
        new_y = self.y - self.speed * sin(radians(self.angle))  # Subtract instead of add
        if not self.check_collision(new_x, new_y):
            self.x = new_x
            self.y = new_y
            
            # consume petrol
            self.petrol -= 2 * self.speed

    def go_back(self):
        
        # Move the tank backward in the direction it's pointing
        new_x = self.x - self.speed * cos(radians(self.angle))
        new_y = self.y + self.speed * sin(radians(self.angle))  # Add instead of subtract
        if not self.check_collision(new_x, new_y):
            self.x = new_x
            self.y = new_y
            
            # consume petrol
            self.petrol -= 2 * self.speed
            
    def rotate(self):
        self.angle = to_principal(self.angle + self.rotate_speed)
        
    def counter_rotate(self):
        self.angle = to_principal(self.angle - self.rotate_speed)

    def check_collision(self, x, y):
        
        # Check if the tank's circular shield is within the screen boundaries
        if (x - self.shield_radius < LEFT_WALL or x + self.shield_radius > RIGHT_WALL or
                y - self.shield_radius < UP_WALL or y + self.shield_radius > DOWN_WALL):
            return True

        # Check for collisions with the enemy tank
        if self.enemy != None:
            distance = calculate_distance(x, y, self.enemy.x, self.enemy.y)
            if distance < self.shield_radius + self.enemy.shield_radius:
                return True

        return False
    

    def check_shoot_success(self):

        cx, cy = WIDTH/2, HEIGHT/2

        x1 = self.x - cx if self.x >= cx else (-1) * (cx - self.x)
        y1 = cy - self.y if self.y <= cy else (-1) * (self.y - cy)
        x2 = self.enemy.x - cx if self.enemy.x >= cx else (-1) * (cx - self.enemy.x)
        y2 = cy - self.enemy.y if self.enemy.y <= cy else (-1) * (self.enemy.y - cy)

        D = calculate_distance(x1, y1, x2, y2)

        print(D)

        K, R = self.shoot_range, self.enemy.shield_radius

        if K < D - R:
            return False

        elif K == D - R:
            angle = degrees(atan2(y2 - y1, x2 - x1))
            print(angle)

            return True if self.angle == angle else False

        elif D - R < K < D:

            angle1 = degrees(atan2(y2 - y1, x2 - x1)) - degrees(acos((D**2 + K**2 - R**2) / (2 * D * K)))
            angle2 = degrees(atan2(y2 - y1, x2 - x1)) + degrees(acos((D**2 + K**2 - R**2) / (2 * D * K)))
            print(angle1, angle2)

            return True if self.angle >= min(angle1, angle2) and self.angle <= max(angle1, angle2) else False

        else:

            angle1 = degrees(atan2(y2 - y1, x2 - x1)) - degrees(asin(R / D))
            angle2 = degrees(atan2(y2 - y1, x2 - x1)) + degrees(asin(R / D))
            
            print(angle1, angle2)

            return True if self.angle >= min(angle1, angle2) and self.angle <= max(angle1, angle2) else False
        
        
    def attack(self):

        print(self.check_shoot_success())


    def delete(self):
        screen.delete(self.body, self.platform, self.cannon, self.shield)


#####################################################################################################

def setInitialValues():
    global tank1, tank2  # objects
    global FPS

    tank1 = Tank(1, LEFT_WALL + 50, UP_WALL + 50, 0)
    tank2 = Tank(2, RIGHT_WALL - 50, DOWN_WALL - 50, 180, tank1)
    tank1.enemy = tank2
    FPS = 120


def keyDownHandler(event):
    keys_pressed[event.keysym] = True


def keyUpHandler(event):
    keys_pressed[event.keysym] = False


def operationsControl():
    if keys_pressed["a"]:
        tank1.rotate()

    if keys_pressed["d"]:
        tank1.counter_rotate()

    if keys_pressed["w"]:
        tank1.go()

    if keys_pressed["s"]:
        tank1.go_back()

    if keys_pressed["Left"]:
        tank2.rotate()

    if keys_pressed["Right"]:
        tank2.counter_rotate()

    if keys_pressed["Up"]:
        tank2.go()

    if keys_pressed["Down"]:
        tank2.go_back()

    if keys_pressed["e"]:
        tank1.attack()

    if keys_pressed["m"]:
        tank2.attack()


def runGame():
    draw_background()
    setInitialValues()

    for f in range(100000):
        operationsControl()

        tank1.draw()
        tank2.draw()
        
        if f % 100 == 0:
        
            data = str(tank1.petrol) + " : " + str(tank2.petrol)
        mytext = screen.create_text(100, 40, text = data, font = "Times 20", fill = "red")

        # update/sleep/delete
        screen.update()
        sleep(1 / FPS)
        tank1.delete()
        tank2.delete()
        screen.delete(mytext)


# Bindings
screen.bind("<Key>", keyDownHandler)
screen.bind("<KeyRelease>", keyUpHandler)

keys_pressed = {
    "a": False, 
    "d": False, 
    "w": False, 
    "s": False, 
    "Left": False, 
    "Right": False, 
    "Up": False, 
    "Down": False, 
    "e" : False, 
    "m" : False, 
    }

screen.focus_set()  # Set focus to the canvas

runGame()

myInterface.mainloop()
