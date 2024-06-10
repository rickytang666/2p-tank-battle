# Importing neccesary packages

from tkinter import *
from math import *
from time import *


# Initializing the screen with constants

WIDTH = 1000
HEIGHT = 800
BACKGROUND_COL = "white"
LEFT_WALL, RIGHT_WALL = 80, WIDTH - 80
UP_WALL, DOWN_WALL = 80, HEIGHT - 80

myInterface = Tk()
screen = Canvas(myInterface, width = WIDTH, height = HEIGHT, background = BACKGROUND_COL)
screen.pack()


################################################################################################


# General drawing/calculating methods

def ConvertAngle(angle):
    return (450 - angle) % 360



def to_principal(angle):

    return (angle + 180) % 360 - 180



def calculate_distance(x1, y1, x2, y2):
    
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)



def rotate_point(centerX, centerY, pointX, pointY, angle):

    # Adjust the angle to follow the mathematical convention
    angle = 90 - angle
    if angle < 0:
        angle += 360

    # Convert the angle to radians
    angle = radians(angle)

    # Translate the point to the origin
    tempX = pointX - centerX
    tempY = pointY - centerY

    # Perform the rotation
    rotatedX = tempX * cos(angle) - tempY * sin(angle)
    rotatedY = tempX * sin(angle) + tempY * cos(angle)

    # Translate the point back to the original location
    finalX = rotatedX + centerX
    finalY = rotatedY + centerY

    return finalX, finalY



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



###################################################################################################


# Classes


class Ammunition:

    def __init__(self, x_pos, y_pos, shoot_range):

        self.x, self.y = x_pos, y_pos
        self.active = False
        self.alive = True

        self.head, self.body = 0, 0
        self.width = 10
        self.speed = 20
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

    def __init__(self, id, x, y, angle, special_technique):

        # Initialize the properties
        self.id = id
        self.name = "Player " + str(self.id)
        self.special_technique = special_technique

        self.color1 = "blue4" if self.id == 1 else "forest green"
        self.color2 = "sky blue" if self.id == 1 else "green2"
        self.length = 40
        self.width = 40
        self.speed = 2
        self.rotate_speed = 1
        self.x = x
        self.y = y
        self.angle = angle
        self.tire_length = self.length * 0.25
        self.tire_width = self.width * 0.2

        self.live_points = 100
        self.hurt = 6
        self.ammunitions_num = 25
        self.ammunitions_used = 0
        self.shield_radius = 26
        self.fuel = 10000
        self.shoot_range = ceil(sqrt(WIDTH ** 2 + HEIGHT ** 2) / 5)
        self.enemy = 0
        self.hit_num = 0
        self.attack_cooldown = 0  # The rate of attacking has limits, just like normal ones
        self.attack_interval = 48
        self.collide_cooldown = 0 # Give the gamer nearly a second to avoid collide

        # Initialize the drawings
        self.body = 0
        self.platform = 0
        self.barrel = 0
        self.shield = 0
        self.shoot_circle = 0
        self.ammunitions = []


    def set_enemy(self, enemy):

        self.enemy = enemy
        # Create the munitions after the enemy is set
        self.ammunitions = [Ammunition(self.x, self.y, self.shoot_range) for _ in range(self.ammunitions_num)]


    def set_special_technique(self):

        if self.special_technique == 1:

            self.technique_name = "Long Shooter"
            self.shoot_range *= 1.5
            
            for ammunition in self.ammunitions:

                ammunition.shoot_range = self.shoot_range

        elif self.special_technique == 2:

            self.technique_name = "Furious Shooter"
            self.hurt = int(1.5 * self.hurt)

        elif self.special_technique == 4:

            self.technique_name = "Resource God"
            self.ammunitions_num += 10

            # reset the ammunitions array

            self.ammunitions = [Ammunition(self.x, self.y, self.shoot_range) for _ in range(self.ammunitions_num)]

        elif self.special_technique == 5:

            self.technique_name = "Juggernaut"
            self.speed /= 2


        elif self.special_technique == 6:

            self.technique_name = "Sports Champion"
            self.fuel *= 2
            self.speed *= 2
            self.rotate_speed *= 2

        elif self.special_technique == 8:

            self.technique_name = "Gatlin"
            self.attack_interval /= 4

        else:

            self.technique_name = "Don't need anything"


    def draw_display_panels(self):

        divide_factor = self.fuel/100

        if self.id == 1:

            self.name_display = screen.create_text(40, 30, text = self.name, font = "Arial 12", fill = self.color1)
            
            self.live_box = screen.create_rectangle(80, 20, 180, 35, fill = "", outline = self.color1, width = 3)
            self.live_bar = screen.create_rectangle(80, 20, 80 + self.live_points, 35, fill = self.color2)

            self.live_display = screen.create_text(200, 30, text = str(self.live_points), font = "Arial 12", fill = self.color1)

            self.fuel_text = screen.create_text(300, 30, text = str(self.fuel) + " mL fuel", font = "Arial 12", fill = self.color1)
            self.fuel_box = screen.create_rectangle(380, 20, 480, 35, fill = "", outline = "black", width = 3)
            self.fuel_bar = screen.create_rectangle(380, 20, 380 + self.fuel/divide_factor, 35, fill = self.color2)

            self.ammunitions_text = screen.create_text(550, 30, text = "Munitions: " + str(self.ammunitions_num), font = "Arial 12", fill = self.color1)

            self.technique_text = screen.create_text(120, 60, text = self.technique_name, font = "Arial 14", fill = "tomato")






        
        else:

            self.name_display = screen.create_text(WIDTH - 40, HEIGHT - 30, text = self.name, font = "Arial 12", fill = self.color1)

            self.live_box = screen.create_rectangle(WIDTH - 180, HEIGHT - 35, WIDTH - 80, HEIGHT - 20, fill = "", outline = self.color1, width = 3)
            self.live_bar = screen.create_rectangle(WIDTH - 180, HEIGHT - 35, WIDTH - 180 + self.live_points, HEIGHT - 20, fill = self.color2)
        
            self.live_display = screen.create_text(WIDTH - 200, HEIGHT - 30, text = str(self.live_points), font = "Arial 12", fill = self.color1)

            self.fuel_text = screen.create_text(WIDTH - 300, HEIGHT - 30, text = str(self.fuel) + " mL fuel", font = "Arial 12", fill = self.color1)

            self.fuel_box = screen.create_rectangle(WIDTH - 480, HEIGHT - 35, WIDTH - 380, HEIGHT - 20, fill = "", outline = "black", width = 3)
            self.fuel_bar = screen.create_rectangle(WIDTH - 480, HEIGHT - 35, WIDTH - 480 + self.fuel/divide_factor, HEIGHT - 20, fill = self.color2)

            self.ammunitions_text = screen.create_text(WIDTH - 550, HEIGHT - 30, text = "Munitions: " + str(self.ammunitions_num), font = "Arial 12", fill = self.color1)

            self.technique_text = screen.create_text(WIDTH - 120, HEIGHT - 60, text = self.technique_name, font = "Arial 14", fill = "tomato")


    def draw(self, frames):
        
        # Every second it show up it should consume fuel
        if frames % 144 == 0 and self.fuel > 0:

            self.fuel -= 1
        
        # Tank components

        self.body = draw_rotated_rectangle(self.x, self.y, self.length, self.width, self.angle, self.color2)
        self.platform = draw_rotated_rectangle(self.x, self.y, self.length * 0.6, self.width * 0.6, self.angle, self.color1)

        self.endX = self.x + 32 * cos(radians(self.angle))
        self.endY = self.y - 32 * sin(radians(self.angle))  # Subtract instead of add
        
        self.barrel = screen.create_line(self.x, self.y, self.endX, self.endY, fill = self.color1, width = 7)
        
        # Draw the tires

        # Calculate the unrotated positions of corners of the tank
        half_length = self.length / 2
        half_width = self.width / 2
        corners = [
            (self.x - half_length, self.y - half_width),
            (self.x - half_length, self.y + half_width),
            (self.x + half_length, self.y - half_width),
            (self.x + half_length, self.y + half_width)
        ]

        # Rotate and draw the tires at the corners
        self.tires = []
        for ox, oy in corners:
            x, y = rotate_point(self.x, self.y, ox, oy, self.angle)
            self.tires.append(draw_rotated_rectangle(x, y, self.tire_length, self.tire_width, self.angle, self.color1))
        
        
        # Draw the display panels

        self.draw_display_panels()
        
        # The shield is for testing and debug
        
        self.shield = draw_circle(self.x, self.y, self.shield_radius, "", "gray")

        # At the first 10 seconds, the game will give each player a feeling of their shooting range

        if frames > 0 and frames <= 144 * 15:

            self.shoot_circle = draw_circle(self.x, self.y, self.shoot_range, "", "orange")


    def draw_munitions(self):

        # Draw the munitions atop the components (better)

        for munition in self.ammunitions:
            if munition.active:
                munition.draw()


    def go(self):

        if self.fuel - self.speed >= 0:

            # Calculate new position
            new_x = self.x + self.speed * cos(radians(self.angle))
            new_y = self.y - self.speed * sin(radians(self.angle))  # Subtract instead of add
            
            # Check collision and handle movement
            if not self.check_slight_collision(new_x, new_y):
                self.x = new_x
                self.y = new_y
                # Consume petrol
                self.fuel -= self.speed


    def go_back(self):

        if self.fuel - self.speed >= 0:
            # Calculate new position
            new_x = self.x - self.speed * cos(radians(self.angle))
            new_y = self.y + self.speed * sin(radians(self.angle))  # Add instead of subtract
            
            # Check collision and handle movement
            if not self.check_slight_collision(new_x, new_y):
                self.x = new_x
                self.y = new_y
                # Consume petrol
                self.fuel -= self.speed

         
    def rotate(self):
        self.angle = to_principal(self.angle + self.rotate_speed)


    def counter_rotate(self):
        self.angle = to_principal(self.angle - self.rotate_speed)


    def check_slight_collision(self, x, y):
        
        if (x - self.shield_radius < LEFT_WALL - 1 or x + self.shield_radius > RIGHT_WALL + 1 or
                y - self.shield_radius < UP_WALL - 1 or y + self.shield_radius > DOWN_WALL + 1):
            
            return True
        
        if self.enemy is not None:
            distance = calculate_distance(x, y, self.enemy.x, self.enemy.y)
            if distance < self.shield_radius + self.enemy.shield_radius - 1:
                return True
        
        return False
    

    def check_rigid_collision(self, x, y):
        
        if (x - self.shield_radius <= LEFT_WALL or x + self.shield_radius >= RIGHT_WALL or
                y - self.shield_radius <= UP_WALL or y + self.shield_radius >= DOWN_WALL):
            
            return True
        
        if self.enemy is not None:
            distance = calculate_distance(x, y, self.enemy.x, self.enemy.y)
            if distance <= self.shield_radius + self.enemy.shield_radius:
                return True
        
        return False


    def collision_penalty(self):

        if self.check_rigid_collision(self.x, self.y):
        
            if self.collide_cooldown == 0:
                if self.live_points > 0:
                    self.live_points -= 1
                self.collide_cooldown = 200  # Reset the cooldown
    

    def check_shoot_success(self):

        cx, cy = WIDTH/2, HEIGHT/2

        x1 = self.x - cx if self.x >= cx else (-1) * (cx - self.x)
        y1 = cy - self.y if self.y <= cy else (-1) * (self.y - cy)
        x2 = self.enemy.x - cx if self.enemy.x >= cx else (-1) * (cx - self.enemy.x)
        y2 = cy - self.enemy.y if self.enemy.y <= cy else (-1) * (self.enemy.y - cy)

        D = calculate_distance(x1, y1, x2, y2)

        K, R = self.shoot_range, self.enemy.shield_radius

        print(D - R)

        if K < D - R:
            return False

        elif K == D - R:
            angle = degrees(atan2(y2 - y1, x2 - x1))

            return True if self.angle == angle else False

        elif D - R < K < D:

            angle1 = degrees(atan2(y2 - y1, x2 - x1)) - degrees(acos((D**2 + K**2 - R**2) / (2 * D * K)))
            angle2 = degrees(atan2(y2 - y1, x2 - x1)) + degrees(acos((D**2 + K**2 - R**2) / (2 * D * K)))
            print(angle1, self.angle, angle2)

            return True if self.angle >= min(angle1, angle2) and self.angle <= max(angle1, angle2) else False

        else:

            angle1 = degrees(atan2(y2 - y1, x2 - x1)) - degrees(asin(R / D))
            angle2 = degrees(atan2(y2 - y1, x2 - x1)) + degrees(asin(R / D))
            
            print(angle1, angle2)

            return True if self.angle >= min(angle1, angle2) and self.angle <= max(angle1, angle2) else False
        
        
    def attack(self):

        if self.attack_cooldown <= 0 and self.fuel >= 30:

            # Every time the barrel works, it will consume energy (fuel in the tank)

            self.fuel -= 30

            if self.ammunitions_num > 0:

                self.ammunitions[self.ammunitions_used].launch(self.angle)

                self.ammunitions_num -= 1
                self.ammunitions_used += 1

                print(self.check_shoot_success())

                if self.check_shoot_success():

                    self.hit_num += 1

                    hurt = self.hurt if self.enemy.special_technique != 5 else floor(self.hurt/2)
                    
                    if self.enemy.live_points - hurt <= 0:
                        self.enemy.live_points = 0
                    else:
                        self.enemy.live_points -= hurt

                self.attack_cooldown = self.attack_interval # reset


    def update(self, enemy):

        # Update the enemy info
        self.enemy = enemy
        
        # Update the max lifespan for each munition
        for munition in self.ammunitions:
            munition.calculate_lifespan(self.enemy)

        # Move and update active munitions
        for munition in self.ammunitions:
            if munition.active:
                munition.move_update()
            else:
                munition.x = self.endX
                munition.y = self.endY

        # Decrease attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.collision_penalty()

        # Decrease collision cooldown
        if self.collide_cooldown > 0:
            self.collide_cooldown -= 1


    def delete(self):

        screen.delete(self.body, self.platform, self.barrel, self.shield)

        screen.delete(*self.tires)

        if self.shoot_circle is not None:

            screen.delete(self.shoot_circle)

        screen.delete(self.name_display, self.live_box, self.live_bar, self.live_display)
        screen.delete(self.fuel_text, self.fuel_box, self.fuel_bar)
        screen.delete(self.ammunitions_text)
        screen.delete(self.technique_text)

        for munition in self.ammunitions:
            munition.delete()



#####################################################################################################

# Actual game-running related functions/procedures


def setInitialValues():

    global tank1, tank2  # objects
    global FPS

    tank1 = Tank(1, LEFT_WALL + 50, UP_WALL + 50, 0, 5)
    tank2 = Tank(2, RIGHT_WALL - 50, DOWN_WALL - 50, 180, 8)
    tank1.set_enemy(tank2)
    tank2.set_enemy(tank1)
    tank1.set_special_technique()
    tank2.set_special_technique()
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

    if keys_pressed["g"]:
        tank1.attack()

    if keys_pressed["m"]:
        tank2.attack()



def checkEndGame():

    if tank1.live_points == 0:

        return 1

    if tank2.live_points == 0:

        return 2
    
    if tank1.fuel == 0 and tank2.fuel == 0:

        return 3
    
    return 0



def victoryDeclare():

    text_positions = [WIDTH/2, HEIGHT/2]

    tank1.draw(0)
    tank2.draw(0)

    if checkEndGame() == 1:
        
        screen.create_text(*text_positions, text = "Player 2 wins", font = "times 20")

    elif checkEndGame() == 2:

        screen.create_text(*text_positions, text = "Player 1 wins", font = "times 20")

    elif checkEndGame() == 3:

        screen.create_text(*text_positions, text = "Both run out of fuel. Draw!", font = "times 20")



def runGame():

    draw_background()
    setInitialValues()

    f = 0

    while True:

        operationsControl()

        tank1.draw(f)
        tank2.draw(f)
        tank1.draw_munitions()
        tank2.draw_munitions()
        tank1.update(tank2)
        tank2.update(tank1)
        

        # update/sleep/delete
        screen.update()
        sleep(1 / FPS)
        tank1.delete()
        tank2.delete()

        f += 1

        if checkEndGame() > 0:

            break

    victoryDeclare()


#####################################################################################################

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
    "g" : False, 
    "m" : False, 
    }

screen.focus_set()  # Set focus to the canvas

#####################################################################################################

# For testing

runGame()

screen.mainloop()