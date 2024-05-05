import pygame
from gameobjects import Rocket, Player
from CONSTANTS import all_obstacles

def check_collisions(player: Player, rocket: Rocket, powerups: pygame.sprite.Group, images: dict) -> tuple[int, int, int]:
    # Collision detection
    if pygame.sprite.spritecollide(rocket, powerups, False): # Maybe haven't collided yet, but powerup is in the boundary rect of rocket
        color = (0, 255, 0, 50)
        current_collisions = pygame.sprite.spritecollide(rocket, powerups, False, pygame.sprite.collide_mask)

        if current_collisions: # Collided
            for powerup in current_collisions:
                powerup_type = powerup.powerup_type
                powerup_level = powerup.level

                if powerup_type == "money":
                    player.money += {1: 1,2: 10, 3: 50}[powerup_level]

                elif powerup_type == "fuel":
                    rocket.fuel += {1: 1, 2: 10, 3: 50}[powerup_level]

                elif powerup_type in all_obstacles:
                    # GAME OVER
                    print(f"""
                          ######################
                          -------GAMEOVER-------
                          ######################
                          Because: {powerup_type}""")
                    rocket.reset()
                    player.money = player.starting_money
                    powerup.position = (0, 100000000)
                    current_collisions = []
                    return color
                    

                if powerup_type == "money" or powerup_type == "fuel":
                    powerup.__init__(powerup_type, powerup_level, (0, 10000), images[None])
                    print("money: " , player.money, "| fuel: ", rocket.fuel)

                
            color = (255,0,0, 50)
    else: # Didn't collide
        color = (0,0,0, 50)
    return color