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


def draw_circle(centerX, centerY, radius, fcol, ocol):
    x1 = centerX - radius
    x2 = centerX + radius
    y1 = centerY - radius
    y2 = centerY + radius
    
    return screen.create_oval(x1, y1, x2, y2, fill = fcol, outline = ocol)

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

def draw_muniton(x, y, width, angle):

    angle = to_principal(angle)

    # Calculate the position of the head of the cannon
    head_x = x + (width) * cos(radians(angle))
    head_y = y - (width) * sin(radians(angle))  # Subtract instead of add

    # Draw the head of the cannon
    head = draw_circle(head_x, head_y, width/2, "orange", "orange")

    # Draw the body of the cannon
    body = draw_rotated_rectangle(x, y, 2 * width, width, angle, "orange")

    
    return [body, head]


###########################################################################


# Classes


class Munition:

    def __init__(self, x_pos, y_pos, shoot_range):

        self.x, self.y = x_pos, y_pos
        self.active = False
        self.alive = True

        self.head, self.body = 0, 0
        self.width = 10
        self.speed = 1
        self.shoot_range = shoot_range
        self.age = 0
        self.angle = 0

    def calculate_lifespan(self, target):

        D = calculate_distance(self.x, self.y, target.x, target.y)

        if self.shoot_range < D:
            self.max_lifespan = ceil(self.shoot_range/self.speed)
        else:
            self.max_lifespan = ceil(D/self.speed)

    def draw(self):

        if self.active:

            angle = to_principal(self.angle)

            # Calculate the position of the head of the cannon
            head_x = self.x + (self.width) * cos(radians(angle))
            head_y = self.y - (self.width) * sin(radians(angle))  # Subtract instead of add

            # Draw the head of the cannon
            self.head = draw_circle(head_x, head_y, self.width/2, "orange", "orange")

            # Draw the body of the cannon
            self.body = draw_rotated_rectangle(self.x, self.y, 2 * self.width, self.width, angle, "orange")

        else:

            self.head, self.body = 0, 0


    def launch(self, angle):

        self.active = True
        self.angle = angle
    

    def move_update(self):
        new_x = self.x + self.speed * cos(radians(self.angle))
        new_y = self.y - self.speed * sin(radians(self.angle))

        if new_x - self.width/2 < LEFT_WALL or new_x + self.width/2 > RIGHT_WALL or \
        new_y - self.width/2 < UP_WALL or new_y + self.width/2 > DOWN_WALL:
            self.alive = False
            self.active = False
        else:
            self.x = new_x
            self.y = new_y
            if self.age >= self.max_lifespan:
                self.alive = False
                self.active = False
            else:
                self.age += 1


    def delete(self):

        if self.head != 0 and self.body != 0:
            screen.delete(self.head, self.body)


class Tank:

    def __init__(self, id, x, y, angle):
        # Initialize the properties
        self.id = id
        self.name = "Player" if self.id == 1 else "Enemy"

        self.color1 = "blue4" if self.id == 1 else "forest green"
        self.color2 = "sky blue" if self.id == 1 else "green2"
        self.length = 45
        self.width = 40
        self.speed = 1
        self.rotate_speed = 0.5
        self.x = x
        self.y = y
        self.angle = angle

        self.live_points = 100
        self.hurt = 6
        self.munitons_num = 20
        self.munitons_used = 0
        self.shield_radius = 28
        self.petrol = 20000
        self.shoot_range = 150
        self.enemy = 0
        self.hit_num = 0
        self.attack_cooldown = 0  # The rate of attacking has limits, just like normal ones

        # Initialize the drawings
        self.body = 0
        self.platform = 0
        self.barrel = 0
        self.shield = 0
        self.shoot_circle = 0
        self.munitons = []

    def set_enemy(self, enemy):

        self.enemy = enemy
        # Create the munitions after the enemy is set
        self.munitons = [Munition(self.x, self.y, self.shoot_range) for _ in range(self.munitons_num)]

    def draw(self):
        
        # Every time it show up it should consume petrol
        self.petrol -= 1
        
        # Tank components

        self.body = draw_rotated_rectangle(self.x, self.y, self.length, self.width, self.angle, self.color2)
        self.platform = draw_rotated_rectangle(self.x, self.y, self.length * 0.6, self.width * 0.6, self.angle, self.color1)

        self.endX = self.x + 30 * cos(radians(self.angle))
        self.endY = self.y - 30 * sin(radians(self.angle))  # Subtract instead of add
        
        self.barrel = screen.create_line(self.x, self.y, self.endX, self.endY, fill=self.color1, width = 7)
        
        # for debug
        
        self.shield = draw_circle(self.x, self.y, self.shield_radius, "", "gray")

        self.shoot_circle = draw_circle(self.x, self.y, self.shoot_range, "", "red")


    def draw_munitions(self):
        # The munitons (if launched)

        for munition in self.munitons:
            if munition.active:
                munition.draw()


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

        if self.munitons_num > 0 and self.attack_cooldown <= 0:

            self.munitons[self.munitons_used].launch(self.angle)

            self.munitons_num -= 1
            self.munitons_used += 1

            print(self.check_shoot_success())

            if self.check_shoot_success():

                self.hit_num += 1
                
                if self.enemy.live_points - self.hurt <= 0:
                    self.enemy.live_points = 0
                else:
                    self.enemy.live_points -= self.hurt

            self.attack_cooldown = 50 # reset

    def update(self):

        # update the max lifespan for each munition

        for munition in self.munitons:

            munition.calculate_lifespan(self.enemy)

        for munition in self.munitons:
            if munition.active:
                munition.move_update()
            else:
                munition.x = self.endX
                munition.y = self.endY

        if self.attack_cooldown > 0:  # If cooldown is active
            self.attack_cooldown -= 1  # Decrease the cooldown

    def delete(self):
        screen.delete(self.body, self.platform, self.barrel, self.shield, self.shoot_circle)

        for muniton in self.munitons:
            muniton.delete()


#####################################################################################################

def setInitialValues():
    global tank1, tank2  # objects
    global FPS

    tank1 = Tank(1, LEFT_WALL + 50, UP_WALL + 50, 0)
    tank2 = Tank(2, RIGHT_WALL - 50, DOWN_WALL - 50, 180)
    tank1.set_enemy(tank2)
    tank2.set_enemy(tank1)
    FPS = 144


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
        keys_pressed["m"] = False

    if keys_pressed["m"]:
        tank2.attack()
        keys_pressed["m"] = False


def runGame():
    draw_background()
    setInitialValues()

    for f in range(100000):
        operationsControl()

        tank1.draw()
        tank2.draw()
        tank1.draw_munitions()
        tank2.draw_munitions()

        tank1.update()
        tank2.update()
        
        if f % 100 == 0:
        
            data = str(tank1.petrol) + " : " + str(tank2.petrol)

        livedata = str(tank1.live_points) + " : " + str(tank2.live_points)

        cannondata = str(tank1.munitons_num) + " : " + str(tank2.munitons_num)

        petroltext = screen.create_text(100, 40, text = data, font = "Times 20", fill = "red")
        livetext = screen.create_text(300, 40, text = livedata, font = "Times 20", fill = "purple")
        cannontext = screen.create_text(500, 40, text = cannondata, font = "Times 20", fill = "tomato")

        # update/sleep/delete
        screen.update()
        sleep(1 / FPS)
        tank1.delete()
        tank2.delete()
        screen.delete(petroltext, livetext, cannontext)


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

screen.mainloop()