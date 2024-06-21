# Author: Ricky Tang
# Created: June 6th, 2024
# Finished: June 20th, 2024

#############################################################################################################
#   GAME OBJECTIVE:
#   The program is organized using classes which provide convenience
#   A two-player tank battle game in a enclosed wall. 
#   Each player used keyborad to control the tank to kill the enemy by taking away all the live points
#   To help winning, the game offers 8 special techniques with bonus functionalities
#   This game provides options to choose different screen sizes, suiting different kinds of computers
#   The game has cool graphics, and have fireworks celebrating the winner at the end of the game
#############################################################################################################

from GameTools import* # Importing the package

TankBattle = Game() # Object of the Game class

TankBattle.runApplication() # Call the running function