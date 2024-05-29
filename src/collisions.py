import pygame
from pygame.math import Vector2
from math import *

from gameobjects import Rocket
from player import Player
from gameobject_scripts import reset_objects
from CONSTANTS import *
from coordinate_systems import *
from bezier_and_map import map_value


def check_collisions(player: Player, rocket: Rocket, collision_group: pygame.sprite.Group, images: dict) -> None:

    current_precollisions = pygame.sprite.spritecollide(rocket, collision_group, False)
    # Collision detection
    if current_precollisions: # Haven't collided yet, but object is in the radius of the rocket

        current_collisions = pygame.sprite.spritecollide(rocket, collision_group, False, pygame.sprite.collide_mask)

        if current_collisions: # Collided
            for object in current_collisions:

                if object.type == "money":
                    player.money += MONEY_VALUES[object.level]

                elif object.type == "fuel":
                    rocket.fuel += FUEL_VALUES[object.level]

                elif object.type in SOLID_OBSTACLES:

                    # GAME OVER
                    print(f"""
                          ######################
                          -------GAMEOVER-------
                          ######################
                          Because: {object.type}""")
                    rocket.reset(player)
                    

                    reset_objects(collision_group, images)

                    object.position = Vector2(0,10000000)
                    current_collisions = []
                    player.deaths += 1
                    player.save_data()

                elif object.type == "cloud" and rocket.disabled == 0:
                    rocket.disabled = map_value(random.random(), 0, 1, MINIMUM_DISABLED, MAXIMUM_DISABLED) # Amount of seconds the rocket will be disabled

                if object.type in COLLECTIBLE_OBJECTS:
                    object.__init__(object.type, object.level, (0, 10000), images[None])
            return True