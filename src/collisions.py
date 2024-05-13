import pygame
from gameobjects import Rocket, Player, create_objects_for_the_first_time, reset_objects
from CONSTANTS import all_obstacles

def check_collisions(player: Player, rocket: Rocket, collision_group: pygame.sprite.Group, images: dict) -> tuple[int, int, int]:

    # Collision detection
    if pygame.sprite.spritecollide(rocket, collision_group, False): # Maybe haven't collided yet, but powerup is in the boundary rect of rocket
        color = (0, 255, 0, 50)
        current_collisions = pygame.sprite.spritecollide(rocket, collision_group, False, pygame.sprite.collide_mask)

        if current_collisions: # Collided
            for object in current_collisions:
                object_type = object.object_type
                object_level = object.level

                if object_type == "money":
                    player.money += {1: 1,2: 10, 3: 50}[object_level]

                elif object_type == "fuel":
                    rocket.fuel += {1: 1, 2: 10, 3: 50}[object_level]

                elif object_type in all_obstacles:
                    # GAME OVER
                    print(f"""
                          ######################
                          -------GAMEOVER-------
                          ######################
                          Because: {object_type}""")
                    rocket.reset()

                    reset_objects(images)

                    print(len(collision_group))

                    player.money = player.starting_money
                    object.position = (0, 100000000)
                    current_collisions = []
                    return color
                    

                if object_type == "money" or object_type == "fuel":
                    object.__init__(object_type, object_level, (0, 10000), images[None])
                    print("money: " , player.money, "| fuel: ", rocket.fuel)

                
            color = (255,0,0, 50)
    else: # Didn't collide
        color = (0,0,0, 50)
    return color