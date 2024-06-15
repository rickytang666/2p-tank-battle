# Importing neccesary packages

from tkinter import *
from math import *
from time import *
from random import *

######################################################################

class General_Methods:

    def __init__(self):
        pass

    
    # MATH

    def ConvertAngle(self, angle):
        return (450 - angle) % 360



    def to_principal(self, angle):

        return (angle + 180) % 360 - 180



    def calculate_distance(self, x1, y1, x2, y2):
        
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)



    def rotate_point(self, centerX, centerY, pointX, pointY, angle):

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


    #############################################################################

    # DRAW

    def draw_circle(self, screen, centerX, centerY, radius, fcol, ocol):
        x1 = centerX - radius
        x2 = centerX + radius
        y1 = centerY - radius
        y2 = centerY + radius
        
        return screen.create_oval(x1, y1, x2, y2, fill = fcol, outline = ocol)



    def draw_rotated_rectangle(self, screen, centerX, centerY, length, width, angle, col):
        # Calculate the corners of the rectangle
        corners = []

        for dx, dy in [(-length / 2, -width / 2), (-length / 2, width / 2), (length / 2, width / 2), (length / 2, -width / 2)]:
            dx_rot = dx * cos(radians(angle)) + dy * sin(radians(angle))
            dy_rot = -dx * sin(radians(angle)) + dy * cos(radians(angle))  # Subtract instead of add
            corners.append((centerX + dx_rot, centerY + dy_rot))

        return screen.create_polygon(*corners, fill=col, outline=col)
    




class Ammunition:

    def __init__(self, x_pos, y_pos, shoot_range, LEFT_WALL, RIGHT_WALL, UP_WALL, DOWN_WALL):

        self.x, self.y = x_pos, y_pos
        self.angle = 0
        self.width = 10
        self.speed = 20

        self.active = False
        self.alive = True

        self.head, self.body = 0, 0
        
        self.shoot_range = shoot_range
        self.age = 0

        self.methods = General_Methods()

        self.LEFT_WALL = LEFT_WALL
        self.RIGHT_WALL = RIGHT_WALL
        self.UP_WALL = UP_WALL
        self.DOWN_WALL = DOWN_WALL
        


    def calculate_lifespan(self, target):

        D = self.methods.calculate_distance(self.x, self.y, target.x, target.y)

        if self.shoot_range < D:
            self.max_lifespan = ceil((self.shoot_range + 32)/self.speed)
        else:
            self.max_lifespan = ceil(D/self.speed)



    def draw(self, screen):

        if self.active:

            angle = self.methods.to_principal(self.angle)

            # Calculate the position of the head of the cannon
            head_x = self.x + (self.width) * cos(radians(angle))
            head_y = self.y - (self.width) * sin(radians(angle))  # Subtract instead of add

            # Draw the head of the cannon
            self.head = self.methods.draw_circle(screen, head_x, head_y, self.width/2, "orange", "orange")

            # Draw the body of the cannon
            self.body = self.methods.draw_rotated_rectangle(screen, self.x, self.y, 2 * self.width, self.width, angle, "orange")

        else:

            self.head, self.body = 0, 0



    def launch(self, angle):

        self.active = True
        self.angle = angle
    


    def move_update(self):
        new_x = self.x + self.speed * cos(radians(self.angle))
        new_y = self.y - self.speed * sin(radians(self.angle))

        if new_x - self.width/2 < self.LEFT_WALL or new_x + self.width/2 > self.RIGHT_WALL or \
        new_y - self.width/2 < self.UP_WALL or new_y + self.width/2 > self.DOWN_WALL:
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



    def delete(self, screen):

        if self.head != 0 and self.body != 0:
            screen.delete(self.head, self.body)






class Tank:

    def __init__(self, id, special_technique, FPS, WIDTH, HEIGHT, LEFT_WALL, RIGHT_WALL, UP_WALL, DOWN_WALL):

        self.methods = General_Methods()

        self.FPS = FPS
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.LEFT_WALL = LEFT_WALL
        self.RIGHT_WALL = RIGHT_WALL
        self.UP_WALL = UP_WALL
        self.DOWN_WALL = DOWN_WALL

        self.id = id
        self.name = "Player " + str(id)
        self.special_technique = special_technique
        self.color1 = "blue4" if self.id == 1 else "forest green"
        self.color2 = "sky blue" if self.id == 1 else "green2"

        self.length = 40
        self.width = 40
        self.barrel_length = 32
        self.tire_length = self.length * 0.25
        self.tire_width = self.width * 0.2

        self.x = self.LEFT_WALL + 50 if self.id == 1 else self.RIGHT_WALL - 50
        self.y = self.UP_WALL + 50 if self.id == 1 else self.DOWN_WALL - 50
        self.speed = 2
        self.rotate_speed = 1
        self.angle = 0 if self.id == 1 else 180

        self.body = 0
        self.platform = 0
        self.barrel = 0
        self.shield = 0
        self.shoot_circle = 0
        self.tires = []

        self.shield_radius = 26
        self.fuel = 10000
        self.full_fuel = self.fuel
        self.live_points = 100
        self.ammunitions_num = 35
        self.ammunitions_used = 0
        self.ammunitions = []

        self.hurt = 6
        self.shoot_range = ceil(sqrt(self.WIDTH ** 2 + self.HEIGHT ** 2) / 5)
        self.attack_cooldown = 0
        self.attack_cooldown = 0 
        self.attack_interval = self.FPS // 3
        self.collide_cooldown = 0
        self.collide_interval = floor(self.FPS * 1.5)
        self.heal_cooldown = 0
        self.heal_interval = floor(self.FPS * 0.6)


    def set_enemy(self, enemy):

        self.set_enemy = enemy

        # Create the ammunitions after the enemy is set

        self.ammunitions = [Ammunition(self.x, self.y, self.shoot_range, self.LEFT_WALL, self.RIGHT_WALL, self.UP_WALL, self.DOWN_WALL) for _ in range(self.ammunitions_num)]



    def set_special_technique(self, technique_names):

        self.technique_name = technique_names[self.special_technique]

        if self.special_technique == 1:
            
            self.shoot_range *= 1.5
            
            for ammunition in self.ammunitions:

                ammunition.shoot_range = self.shoot_range


        elif self.special_technique == 2:
            
            self.hurt = int(1.5 * self.hurt)
            self.ammunitions_num -= 5
            self.ammunitions = [Ammunition(self.x, self.y, self.shoot_range, self.LEFT_WALL, self.RIGHT_WALL, self.UP_WALL, self.DOWN_WALL) for _ in range(self.ammunitions_num)]


        elif self.special_technique == 3:

            self.speed = floor(self.speed * 0.5)
            self.fuel = floor(self.fuel * 0.5)
            self.full_fuel = self.fuel
            self.shoot_range = floor(self.shoot_range * 0.7)

            for ammunition in self.ammunitions:

                ammunition.shoot_range = self.shoot_range


        elif self.special_technique == 4:
            
            self.ammunitions_num += 10

            # reset the ammunitions array

            self.ammunitions = [Ammunition(self.x, self.y, self.shoot_range, self.LEFT_WALL, self.RIGHT_WALL, self.UP_WALL, self.DOWN_WALL) for _ in range(self.ammunitions_num)]


        elif self.special_technique == 5:

            self.speed /= 2


        elif self.special_technique == 6:
            
            self.fuel = ceil(self.fuel * 1.5)
            self.full_fuel = self.fuel
            self.speed = ceil(self.speed * 1.5)
            self.rotate_speed = ceil(self.speed * 1.5)


        elif self.special_technique == 8:

            self.technique_name = "Gatlin"
            self.attack_interval /= 4



    def draw_display_panels(self, screen):

        fuel_length = 0 if self.fuel == 0 else (self.fuel/self.full_fuel) * 100

        if self.id == 1:

            self.name_display = screen.create_text(40, 25, text = self.name, font = "Arial 12", fill = self.color1)
            
            self.live_box = screen.create_rectangle(80, 15, 180, 30, fill = "", outline = self.color1, width = 3)
            self.live_bar = screen.create_rectangle(80, 15, 80 + self.live_points, 30, fill = self.color2)
            self.live_display = screen.create_text(200, 25, text = str(self.live_points), font = "Arial 10", fill = self.color1)

            self.fuel_text = screen.create_text(280, 25, text = str(self.fuel) + " mL fuel", font = "Arial 10", fill = self.color1)
            self.fuel_box = screen.create_rectangle(330, 15, 430, 30, fill = "", outline = "black", width = 3)
            self.fuel_bar = screen.create_rectangle(330, 15, 330 + fuel_length, 30, fill = self.color2)

            self.ammunitions_text = screen.create_text(500, 25, text = "Ammunitions: " + str(self.ammunitions_num), font = "Arial 10", fill = self.color1)

            self.technique_text = screen.create_text(120, 50, text = self.technique_name, font = "Arial 12", fill = "tomato")



        
        else:

            self.name_display = screen.create_text(self.WIDTH - 40, self.HEIGHT - 25, text = self.name, font = "Arial 12", fill = self.color1)

            self.live_box = screen.create_rectangle(self.WIDTH - 180, self.HEIGHT - 30, self.WIDTH - 80, self.HEIGHT - 15, fill = "", outline = self.color1, width = 3)
            self.live_bar = screen.create_rectangle(self.WIDTH - 180, self.HEIGHT - 30, self.WIDTH - 180 + self.live_points, self.HEIGHT - 15, fill = self.color2)
            self.live_display = screen.create_text(self.WIDTH - 200, self.HEIGHT - 25, text = str(self.live_points), font = "Arial 10", fill = self.color1)

            self.fuel_text = screen.create_text(self.WIDTH - 280, self.HEIGHT - 25, text = str(self.fuel) + " mL fuel", font = "Arial 10", fill = self.color1)
            self.fuel_box = screen.create_rectangle(self.WIDTH - 430, self.HEIGHT - 30, self.WIDTH - 330, self.HEIGHT - 15, fill = "", outline = "black", width = 3)
            self.fuel_bar = screen.create_rectangle(self.WIDTH - 430, self.HEIGHT - 30, self.WIDTH - 430 + fuel_length, self.HEIGHT - 15, fill = self.color2)

            self.ammunitions_text = screen.create_text(self.WIDTH - 500, self.HEIGHT - 25, text = "Ammunitions: " + str(self.ammunitions_num), font = "Arial 10", fill = self.color1)

            self.technique_text = screen.create_text(self.WIDTH - 120, self.HEIGHT - 50, text = self.technique_name, font = "Arial 12", fill = "tomato")



    def draw(self, screen, frames):
        
        # Every second it show up it should consume fuel
        if frames % 144 == 0 and self.fuel > 0:

            self.fuel -= 1
        
        # TANK COMPONENTS

        self.body = self.methods.draw_rotated_rectangle(screen, self.x, self.y, self.length, self.width, self.angle, self.color2)
        self.platform = self.methods.draw_rotated_rectangle(screen, self.x, self.y, self.length * 0.6, self.width * 0.6, self.angle, self.color1)

        self.endX = self.x + self.barrel_length * cos(radians(self.angle))
        self.endY = self.y - self.barrel_length * sin(radians(self.angle))  # Subtract instead of add because of tkinter angle system
        
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

        self.tires = [] # reset it to empty every time
        for ox, oy in corners:
            x, y = self.methods.rotate_point(self.x, self.y, ox, oy, self.angle)
            self.tires.append(self.methods.draw_rotated_rectangle(screen, x, y, self.tire_length, self.tire_width, self.angle, self.color1))
        
        
        # Draw the display panels

        self.draw_display_panels(screen)
        
        # The shield is for testing and debug
        
        # self.shield = draw_circle(self.x, self.y, self.shield_radius, "", "gray")

        # At the first 10 seconds, the game will give each player a feeling of their shooting range

        if frames > 0 and frames <= 144 * 15:

            self.shoot_circle = self.methods.draw_circle(screen, self.x, self.y, self.shoot_range, "", "orange")

    

    def draw_ammunitions(self, screen):

        # Draw the munitions atop the components (better)

        for ammunition in self.ammunitions:
            if ammunition.active:
                ammunition.draw(screen)



    def check_slight_collision(self, x, y):
        
        if (x - self.shield_radius < self.LEFT_WALL - 1 or x + self.shield_radius > self.RIGHT_WALL + 1 or
                y - self.shield_radius < self.UP_WALL - 1 or y + self.shield_radius > self.DOWN_WALL + 1):
            
            return True
        
        if self.enemy is not None:
            distance = self.methods.calculate_distance(x, y, self.enemy.x, self.enemy.y)
            if distance < self.shield_radius + self.enemy.shield_radius - 1:
                return True
        
        return False
    


    def check_rigid_collision(self, x, y):
        
        if (x - self.shield_radius <= self.LEFT_WALL or x + self.shield_radius >= self.RIGHT_WALL or
                y - self.shield_radius <= self.UP_WALL or y + self.shield_radius >= self.DOWN_WALL):
            
            return True
        
        if self.enemy is not None:
            distance = self.methods.calculate_distance(x, y, self.enemy.x, self.enemy.y)
            if distance <= self.shield_radius + self.enemy.shield_radius:
                return True
        
        return False



    def collision_penalty(self):

        if self.check_rigid_collision(self.x, self.y):
        
            if self.collide_cooldown == 0:
                if self.live_points > 0:
                    self.live_points -= 1
                self.collide_cooldown = self.collide_interval  # Reset the cooldown



    def heal_handler(self):

        # Increase self heal cooldown

        if self.heal_cooldown < self.heal_interval:

            self.heal_cooldown += 1

        else:

            if self.live_points < self.heal_interval:

                self.live_points += 1

                self.heal_cooldown = 0


    
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

                if self.special_technique == 7:
                    self.heal_handler()



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
            
                if self.special_technique == 7:
                    self.heal_handler()



    def rotate(self):
        self.angle = self.methods.to_principal(self.angle + self.rotate_speed)



    def counter_rotate(self):
        self.angle = self.methods.to_principal(self.angle - self.rotate_speed)



    def calculate_absolute_angle(self):

        cx, cy = self.WIDTH/2, self.HEIGHT/2

        x1 = self.x - cx if self.x >= cx else (-1) * (cx - self.x)
        y1 = cy - self.y if self.y <= cy else (-1) * (self.y - cy)
        x2 = self.enemy.x - cx if self.enemy.x >= cx else (-1) * (cx - self.enemy.x)
        y2 = cy - self.enemy.y if self.enemy.y <= cy else (-1) * (self.enemy.y - cy)

        return degrees(atan2(y2 - y1, x2 - x1))
    


    def check_shoot_success(self):

        cx, cy = self.WIDTH/2, self.HEIGHT/2

        x1 = self.x - cx if self.x >= cx else (-1) * (cx - self.x)
        y1 = cy - self.y if self.y <= cy else (-1) * (self.y - cy)
        x2 = self.enemy.x - cx if self.enemy.x >= cx else (-1) * (cx - self.enemy.x)
        y2 = cy - self.enemy.y if self.enemy.y <= cy else (-1) * (self.enemy.y - cy)

        D = self.methods.calculate_distance(x1, y1, x2, y2)

        K, R = self.shoot_range, self.enemy.shield_radius

        # print(D - R)

        if self.special_technique == 3:

            return True if K >= D - R else False
        
        else: 

            if K < D - R:
                return False

            elif K == D - R:
                angle = degrees(atan2(y2 - y1, x2 - x1))

                return True if self.angle == angle else False

            elif D - R < K < D:

                angle1 = degrees(atan2(y2 - y1, x2 - x1)) - degrees(acos((D**2 + K**2 - R**2) / (2 * D * K)))
                angle2 = degrees(atan2(y2 - y1, x2 - x1)) + degrees(acos((D**2 + K**2 - R**2) / (2 * D * K)))
                
                # print(angle1, self.angle, angle2)

                return True if self.angle >= min(angle1, angle2) and self.angle <= max(angle1, angle2) else False

            else:

                angle1 = degrees(atan2(y2 - y1, x2 - x1)) - degrees(asin(R / D))
                angle2 = degrees(atan2(y2 - y1, x2 - x1)) + degrees(asin(R / D))
                
                # print(angle1, angle2)

                return True if self.angle >= min(angle1, angle2) and self.angle <= max(angle1, angle2) else False
    

        
    def attack(self):

        if self.attack_cooldown <= 0 and self.fuel >= 30:

            # Every time the barrel works, it will consume energy (fuel in the tank)

            self.fuel -= 30

            if self.ammunitions_num > 0:

                if self.special_technique == 3:

                    self.ammunitions[self.ammunitions_used].launch(self.calculate_absolute_angle())

                else: 
                
                    self.ammunitions[self.ammunitions_used].launch(self.angle)

                self.ammunitions_num -= 1
                self.ammunitions_used += 1

                # print(self.check_shoot_success())

                if self.check_shoot_success():

                    hurt = self.hurt if self.enemy.special_technique != 5 else floor(self.hurt/2)
                    
                    if self.enemy.live_points - hurt <= 0:
                        self.enemy.live_points = 0
                    else:
                        self.enemy.live_points -= hurt

                self.attack_cooldown = self.attack_interval # reset



    def update(self, enemy):

        # Update the enemy info
        self.enemy = enemy
        
        
        for ammunition in self.ammunitions:

            # Update the max lifespan for each munition

            ammunition.calculate_lifespan(self.enemy)

            # if active, update position to animate; if not, update position with the tank

            if ammunition.active:
                ammunition.move_update()
            else:
                ammunition.x = self.x
                ammunition.y = self.y

        

        # Decrease attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Monitor collision and give penalty if applicable

        self.collision_penalty()

        # Decrease collision cooldown
        if self.collide_cooldown > 0:
            self.collide_cooldown -= 1



    def delete(self, screen):

        screen.delete(self.body, self.platform, self.barrel)
        screen.delete(*self.tires)

        if self.shield is not None:

            screen.delete(self.shield)

        if self.shoot_circle is not None:

            screen.delete(self.shoot_circle)

        screen.delete(self.name_display, self.live_box, self.live_bar, self.live_display)
        screen.delete(self.fuel_text, self.fuel_box, self.fuel_bar)
        screen.delete(self.ammunitions_text)
        screen.delete(self.technique_text)

        for munition in self.ammunitions:
            munition.delete(screen)






class Game:

    def __init__(self):

        self.myInterface = Tk()

        self.methods = General_Methods()

        self.WIDTH = 650
        self.HEIGHT = round((4/5) * self.WIDTH / 50) * 50
        self.LEFT_WALL, self.RIGHT_WALL = 80, self.WIDTH - 80
        self.UP_WALL, self.DOWN_WALL = 80, self.HEIGHT - 80
        self.BACKGROUND_COL = "white"
        self.FPS = 144
        self.screen_widths = {

            "Chromebook" : 650,
            "Small Laptop" : 800,
            "Big Laptop" : 1000,
            "Desktop" : 1200,

        }


        self.menu_screen = 0
        self.game_screen = 0

        self.keys_pressed = {
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

        self.tank1 = 0
        self.tank2 = 0
        self.technique1, self.technique2 = 0, 0


        self.technique_names = {

            0 : "Don't need anything",
            1 : "Long Shooter",
            2 : "Furious Shooter",
            3 : "Auto-Aiming",
            4 : "Resource God",
            5 : "Juggernaut",
            6 : "Sport Champion",
            7 : "Self Heal",
            8 : "Gatlin"

        }

        self.technique_descriptions = {

            1 : "Longer shoot range",
            2 : "Greater shoot hurt, but fewer ammunitions",
            3 : "The tank aims the opponent for you, but slower speed and shorter shoot range",
            4 : "10 more ammunitions",
            5 : "Only half hurt when being hit, but also half speed",
            6 : "Greater speed, fuel, and rotating speed -> More flexible",
            7 : "Recover live points when you move",
            8 : "Greater shooting frequency possible"

        }


        self.player_turn = 1
        self.game_running = False

        self.endgame_texts = {

            1 : "Player 2 wins!",
            2 : "Player 1 wins!",
            3 : "Both run out of fuel. Draw!"

        }



    # SCREENSIZE SELECTIONS



    def initialize_game_screen(self):

        self.HEIGHT = round((4/5) * self.WIDTH / 50) * 50
        self.LEFT_WALL, self.RIGHT_WALL = 80, self.WIDTH - 80
        self.UP_WALL, self.DOWN_WALL = 80, self.HEIGHT - 80

        self.game_screen = Canvas(self.myInterface, width = self.WIDTH, height = self.HEIGHT, background = self.BACKGROUND_COL)
        self.game_screen.pack()



    def show_screensize_select(self):
        
        self.menu_screen = Canvas(self.myInterface, width = 300, height = 300, bg = "white")
        self.menu_screen.pack()

        self.menu_screen.create_text(150, 25, text = "Please choose your computer type", font = "Arial 10")

        x, y = 200, 75
        for key, value in self.screen_widths.items():
            self.create_button(key, value, x, y)
            y += 50  # Adjust y-coordinate for next button


        game.menu_screen.mainloop()


    
    def on_screensize_click(self, value):

        self.WIDTH = value

        self.menu_screen.destroy()

        self.initialize_game_screen()

        self.startApplication()



    def create_button(self, key, value, x, y):
        
        button = Button(self.menu_screen, text = key, command = lambda : self.on_screensize_click(value))
        self.menu_screen.create_window(x, y, window = button, anchor = E)



    # BEFORE GAME GREETINGS & PREP


    
    def show_rules(self):
        self.game_screen.delete("all")
        self.game_screen.create_text(self.WIDTH/2, 25, text="Rules", font="Arial 16")
        self.back_button = Button(self.game_screen, text="Back", command=self.back_to_homescreen)
        self.game_screen.create_window(self.WIDTH - 50, self.HEIGHT - 50, window=self.back_button)



    def show_techniques(self):

        self.game_screen.delete("all")
        self.game_screen.create_text(self.WIDTH/2, 25, text="Special Techniques", font="Arial 16")


        for i in range(1, 9):

            self.game_screen.create_text(self.WIDTH/2, 20 + i * 50, text = self.technique_names[i], font = "Arial 12")
            self.game_screen.create_text(self.WIDTH/2, 38 + i * 50, text = self.technique_descriptions[i], font = "Arial 10", fill = "blue")


        self.back_button = Button(self.game_screen, text="Back", command=self.back_to_homescreen)
        self.game_screen.create_window(self.WIDTH - 50, self.HEIGHT - 50, window=self.back_button)



    def back_to_homescreen(self):
        self.game_screen.delete("all")
        self.startApplication()



    def startApplication(self):
        self.welcome_text = self.game_screen.create_text(self.WIDTH/2, self.HEIGHT/2, text="Welcome! (Press space to start, Press Esc to quit)", font="Arial 16")
        self.rules_button = Button(self.game_screen, text="Rules", command=self.show_rules)
        self.game_screen.create_window(self.WIDTH/2, self.HEIGHT - 100, window=self.rules_button)
        self.special_techniques_button = Button(self.game_screen, text="Special Techniques", command=self.show_techniques)
        self.game_screen.create_window(self.WIDTH/2, self.HEIGHT - 50, window=self.special_techniques_button)
        self.game_screen.bind('<space>', self.startGame)
        self.game_screen.bind('<Escape>', self.quitGame)
        self.game_screen.focus_set()



    def startGame(self, event):

        if not self.game_running:
            self.game_screen.delete(self.welcome_text)
            self.rules_button.destroy()
            self.special_techniques_button.destroy()
            self.player_turn = 1
            self.technique_selection()



    def technique_selection(self):

        self.technique_buttons = []

        for i in range(9):

            button = Button(self.game_screen, text=str(self.technique_names[i]), command=lambda i=i: self.on_technique_click(i))
            self.technique_buttons.append(button)
            self.game_screen.create_window(300, 75 + i * 35, window = button)

        # Add instructions for the players
        player_name = "First" if self.player_turn == 1 else "Second"
        self.select_instructions = self.game_screen.create_text(self.WIDTH/2, 25, text=f"{player_name} player, please choose technique", font="Arial 12")



    def on_technique_click(self, technique):

        if self.player_turn == 1:

            self.technique1 = technique

            self.player_turn = 2 # Switch to the second player after assigning

            # Remove player 1's buttons and instructions

            for button in self.technique_buttons: button.destroy()

            self.game_screen.delete(self.select_instructions)
            self.technique_buttons.clear()

            # Show player 2's buttons
            self.technique_selection()

        
        else:

            self.technique2 = technique

            # Remove player 2's buttons and instructions
            for button in self.technique_buttons: button.destroy()

            self.game_screen.delete(self.select_instructions)
            self.technique_buttons.clear()


            # Start the game
            self.game_running = True
            self.runGame()



    def setTanks(self):

        self.tank1 = Tank(1, self.technique1, self.FPS, self.WIDTH, self.HEIGHT, self.LEFT_WALL, self.RIGHT_WALL, self.UP_WALL, self.DOWN_WALL)
        self.tank2 = Tank(2, self.technique2, self.FPS, self.WIDTH, self.HEIGHT, self.LEFT_WALL, self.RIGHT_WALL, self.UP_WALL, self.DOWN_WALL)

        self.tank1.set_enemy(self.tank2)
        self.tank2.set_enemy(self.tank1)
        self.tank1.set_special_technique(self.technique_names)
        self.tank2.set_special_technique(self.technique_names)



    # KEY CONTROL


    def keyDownHandler(self, event):

        self.keys_pressed[event.keysym] = True



    def keyUpHandler(self, event):

        self.keys_pressed[event.keysym] = False


    
    def operationsControl(self):

        if self.keys_pressed["a"]:
            self.tank1.rotate()

        if self.keys_pressed["d"]:
            self.tank1.counter_rotate()

        if self.keys_pressed["w"]:
            self.tank1.go()

        if self.keys_pressed["s"]:
            self.tank1.go_back()

        if self.keys_pressed["Left"]:
            self.tank2.rotate()

        if self.keys_pressed["Right"]:
            self.tank2.counter_rotate()

        if self.keys_pressed["Up"]:
            self.tank2.go()

        if self.keys_pressed["Down"]:
            self.tank2.go_back()

        if self.keys_pressed["g"]:
            self.tank1.attack()

        if self.keys_pressed["m"]:
            self.tank2.attack()



    def game_bindings(self):

        self.game_screen.bind("<Key>", self.keyDownHandler)
        self.game_screen.bind("<KeyRelease>", self.keyUpHandler)

        self.game_screen.focus_set()



    # POST-GAME



    def checkEndGame(self):

        if self.tank1.live_points == 0:

            return 1

        if self.tank2.live_points == 0:

            return 2
        
        if self.tank1.fuel == 0 and self.tank2.fuel == 0:

            return 3
        
        return 0
    

    
    def endgame_process(self):

        text_positions = [self.WIDTH/2, self.HEIGHT/2]

        self.tank1.draw_display_panels(self.game_screen)
        self.tank2.draw_display_panels(self.game_screen)

        endgame_text = self.endgame_texts[self.checkEndGame()]

        self.game_screen.create_text(*text_positions, text = endgame_text, font = "Arial 20")

        self.hint_text = self.game_screen.create_text(self.WIDTH/2, self.HEIGHT/2 + 50, text="(Press space to return to homepage, Press Esc to quit)", font = "Arial 12")
        self.game_screen.bind('<space>', self.replayGame)
        self.game_screen.bind('<Escape>', self.quitGame)
        self.game_screen.focus_set()



    # GAME ENVIRONMENT DRAWINGS


    
    def draw_walls(self):

        self.game_screen.create_rectangle(self.LEFT_WALL, self.UP_WALL, self.RIGHT_WALL, self.DOWN_WALL, fill = "", width = 5)




    # GENERAL RUNNINGS



    def quitGame(self, event):
        self.myInterface.quit()



    def replayGame(self, event):
        self.game_screen.delete("all")
        self.startApplication()



    def runGame(self):

        self.game_bindings()
        self.setTanks()
        self.draw_walls()


        f = 0

        while True:

            self.operationsControl()

            self.tank1.draw(self.game_screen, f)
            self.tank2.draw(self.game_screen, f)
            self.tank1.draw_ammunitions(self.game_screen)
            self.tank2.draw_ammunitions(self.game_screen)


            self.tank1.update(self.tank2)
            self.tank2.update(self.tank1)
            self.game_screen.update()

            sleep(1 / self.FPS)

            self.tank1.delete(self.game_screen)
            self.tank2.delete(self.game_screen)

            f += 1



            if self.checkEndGame() > 0:
                self.game_running = False
                break

        
        self.endgame_process()



    def runApplication(self):
        self.show_screensize_select()


#####################################################################

# FOR TESTING

game = Game()

game.runApplication()