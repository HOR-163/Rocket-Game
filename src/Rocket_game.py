""" GOOD SOURCES FOR FUTURE """
# Gravity, physics: https://www.youtube.com/watch?v=5j0uU3aJxJM
# Camera control: https://www.youtube.com/watch?v=u7LPRqrzry8
# Collisions: https://www.youtube.com/watch?v=tJiKYMQJnYg
# Background scrolling/tiling: https://youtu.be/ARt6DLP38-Y

"""Start of the actual program"""
import pygame
# For antialiasing one day (maybe)
#import pygame.gfxdraw
from math import *
import os
import time
import random

from CONSTANTS import *
from bezier import *
from coordinate_systems import *
from gameobjects import *
from collisions import check_collisions
import debug
DEBUG = True

"""######################################################################
   Initialize the pygame module and attributes that are related to it.
######################################################################"""
pygame.init()
screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption("Rocket Game")
fps = 60
timer = pygame.time.Clock()

# Set some global variables for the rockets
scale = 1


# Define the debug font
debug_font = pygame.font.SysFont('consolas', 15)

"""#################################################
   Load all images, that are needed for the game.
#################################################"""
path = os.getcwd()
# For IDLE uncomment the following line (in VSCode comment this line)
#path = path[:path.rfind("\\") + 1] # <------- This one
missing_texture = pygame.image.load(path + "\\images\\missing_texture.png").convert_alpha()

rocket_image_og = pygame.image.load(path + "\\images\\rocket2.png").convert_alpha()

coin_img = pygame.image.load(path + "\\images\\coin.png").convert_alpha()
cash_img = pygame.image.load(path + "\\images\\cash.png").convert_alpha()
money_bag_img = pygame.image.load(path + "\\images\\money_bag.png").convert_alpha()

small_fuel_img = pygame.image.load(path + "\\images\\small_fuel.png").convert_alpha()
medium_fuel_img = pygame.image.load(path + "\\images\\medium_fuel.png").convert_alpha()
large_fuel_img = pygame.image.load(path + "\\images\\large_fuel.png").convert_alpha()


images = {1: coin_img, 2: cash_img, 3: money_bag_img,
          4: small_fuel_img, 5: medium_fuel_img, 6: large_fuel_img,
          # Obstacles
          "plane": missing_texture, "helicopter": missing_texture, "hot_air_balloon": missing_texture, "cloud": missing_texture, #level 1
          "fighter_jet": missing_texture,   # level 2
          "UFO": missing_texture, "satellite": missing_texture, #level 3
          None: missing_texture} 

def map_color(x: float, in_min: float, in_max: float, out_min: float, out_max: float):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def gradient(y: int):
    color1 = (176, 230, 235)
    color2 = (0,0,255)
    color3 = (0,0,0)
    stop1 = 0
    stop2 = 150
    stop3 = 300

    result = color3

    if stop1 <= y < stop2:
        percent = map_color(y, stop1, stop2, 0, 1)
        result = (color1[0] + percent * (color2[0] - color1[0]),
                  color1[1] + percent * (color2[1] - color1[1]),
                  color1[2] + percent * (color2[2] - color1[2]))
    elif stop2 <= y < stop3:
        percent = map_color(y, stop2, stop3, 0, 1)
        result = (color2[0] + percent * (color3[0] - color2[0]),
                  color2[1] + percent * (color3[1] - color2[1]),
                  color2[2] + percent * (color3[2] - color2[2]))
    return result


class Background:
    """Handle background."""

    def __init__(self, load_x: int, load_y: int):
        # how many chunks to load (e.g 3x3 amount of chunks)
        self.load_x = load_x
        self.load_y = load_y

    def update(self, rocket_position: tuple[float, float]):
        chunk_x, chunk_y = world_to_chunk_coordinates(rocket_position)
        #chunk_y += int((self.load_y - 1) / 2)
        for y_offset in range(int(-self.load_y / 2), int(self.load_y / 2) + 1):
            background = gradient(chunk_y + y_offset)
            for x_offset in range(int(-self.load_x / 2), int(self.load_x / 2) + 1):

                world_x, world_y = chunk_to_world_coordinates((chunk_x + x_offset, -chunk_y - y_offset))

                chunk_screen_coordinates = world_to_screen_coordinates((world_x, -world_y), rocket_position, scale)

                # Draw the rectangles
                if chunk_y + y_offset >= 0:
                    pygame.draw.rect(screen, background, pygame.Rect(chunk_screen_coordinates[0], chunk_screen_coordinates[1], 
                                                                ceil(C_WIDTH * scale), ceil(C_HEIGHT * scale)))


                # Draw the ground
                elif chunk_y + y_offset < 0:
                    pygame.draw.rect(screen, GROUND_COLOR, pygame.Rect(chunk_screen_coordinates[0], chunk_screen_coordinates[1], 
                                                                        ceil(C_WIDTH * scale), ceil(C_HEIGHT * scale)))
                
                if DEBUG:
                    # Create and find the size (length, height) of chunk text (mainly for debugging)
                    chunk_coordinates_str = f"{chunk_x + x_offset} {chunk_y + y_offset}"
                    chunk_coordinates_rendered = debug_font.render(chunk_coordinates_str, True, 'black', 'white')
                    chunk_coordinates_str_size = debug_font.size(chunk_coordinates_str)
                    chunk_coordinates_str_coordinates = (chunk_screen_coordinates[0] + C_WIDTH / 2 * scale - chunk_coordinates_str_size[0] / 2, 
                                                         chunk_screen_coordinates[1] + C_HEIGHT / 2 * scale - chunk_coordinates_str_size[1] / 2)
                    # Write the chunk coordinates to the screen (uses basically the same equations like in background drawing)
                    screen.blit(chunk_coordinates_rendered, chunk_coordinates_str_coordinates)

                    # Draw chunk borders
                    pygame.draw.rect(screen, 'red', pygame.Rect(chunk_screen_coordinates[0], chunk_screen_coordinates[1], 
                                            ceil(C_WIDTH * scale), ceil(C_HEIGHT * scale)), 1)

        # For debugging
        return (chunk_x, chunk_y)


def input():
    """ Keyboard input handling."""
    keys = pygame.key.get_pressed()

    # For debug fps changer
    global fps
    global highest_dt

    if keys[pygame.K_1]:
        fps = 30
        highest_dt = 0.001
    elif keys[pygame.K_2]:
        fps = 60
        highest_dt = 0.001
    elif keys[pygame.K_3]:
        fps = 120
        highest_dt = 0.001
    # Unlimited fps
    elif keys[pygame.K_4]:
        fps = 0
        highest_dt = 0.001
    elif keys[pygame.K_0]:
        fps = 1
        highest_dt = 0.001

    
    return keys



""" # Points on the corners of the rocket (size in px, coords origin is the center of the rocket)
collision_points = [[-25,50],[25,50],[-25,-50],[25,-50]]
#                 start_x,  start_y,    acceleration,
#                    |         |        |  boost acceleration,
#                    |         |        |  |   maximum speed
#                    |         |        |  |   |    points for collision
#                    |         |        |  |   |    |
rocket = Rocket(WIDTH / 2, HEIGHT / 2, 4, 8, 2000, collision_points, rocket_image_og) """

collision_points = [[1,49],[25,-1],[13,-50],[-11,-50], [-23,-1]]
#                 start_x,  start_y,    acceleration,
#                    |         |        |  boost acceleration,
#                    |         |        |  |   maximum speed
#                    |         |        |  |   |    start_fuel
#                    |         |        |  |   |    |           points for collision
#                    |         |        |  |   |    |           |               image
#                    |         |        |  |   |    |           |               |
rocket = Rocket(WIDTH / 2, HEIGHT / 2, 4, 8, 2000, 100, collision_points, rocket_image_og) 

# Make a player object (currently used only for money storage)
player = Player()

background = Background(9,9)

first = True

run = True
color = (0,0,0)

time1, time2 = 0,0

highest_dt = 0.0
dt = 0.016

while run:
    if first:
        create_objects_for_the_first_time(images)

    # For FPS counter
    real_dt = (time.perf_counter_ns() - time1) / 1_000_000_000 # Because it is in nanoseconds

    if real_dt >= highest_dt and not first:
        highest_dt = real_dt
    time1 = time.perf_counter_ns()


    dt = 0.016

    # Fill the screen with background color
    screen.fill(SKY_COLOR)
    
    # Get input from keyboard mouse (HID)
    keys = input()

    collision_color = check_collisions(player, rocket, collision_group, images)


    # Update background
    chunk_coordinates = background.update(rocket.position)

    # Calculate new rocket position and draw the rocket
    speed = rocket.update(screen, dt, scale, keys, collision_color)

    update_objects(chunk_coordinates, images)

    rocket_position = rocket.position
    for object in collision_group:
        object.draw(screen, scale, rocket_position)





    # Calculate the scale 
    scale = cubic_bezier(0, 0, 50, 0, 100, 100, 50, 100, speed / rocket.max_speed) / 100 + 1

    # For debug info
    if not first and DEBUG == True:
        debug.info(screen, debug_font, rocket, last_speed, chunk_coordinates, scale, real_dt, highest_dt)
    else:
        first = False

    last_speed = rocket.x_speed, rocket.y_speed

    # Read HID inputs ONLY FOR QUITTING THE GAME
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            run = False
        if event.type == pygame.KEYUP and keys[pygame.K_F1]:
            DEBUG = not DEBUG
            rocket.debug = DEBUG




    # Update the screen
    pygame.display.update()

    # Apply running fps
    dt = timer.tick(fps) * 0.001
    
pygame.quit()
            
    
        
