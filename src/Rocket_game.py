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
from CONSTANTS import *
from bezier import *
from coordinate_systems import *
from gameobjects import *
import debug

#Initialize the pygame module and attributes that are related to it
pygame.init()

# Initialize the game
screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption("Rocket Game")
fps = 60
timer = pygame.time.Clock()



# Set some global variables for the rockets
scale = 1

# Define the debug font
debug_font = pygame.font.SysFont('consolas', 15)

# load the rocket image
path = os.getcwd()
# For IDLE uncomment the following line (in VSCode comment this line)
#path = path[:path.rfind("\\") + 1] # <------- This one
rocket_image_og = pygame.image.load(path + "\\images\\rocket1.png").convert_alpha()
coin_img = pygame.image.load(path + "\\images\\coin.png").convert_alpha()
cash_img = pygame.image.load(path + "\\images\\cash.png").convert_alpha()
money_bag_img = pygame.image.load(path + "\\images\\money_bag.png").convert_alpha()

class Background:
    """Handle background."""

    def __init__(self, load_x: int, load_y: int):
        # how many chunks to load (e.g 3x3 amount of chunks)
        self.load_x = load_x
        self.load_y = load_y

    def update(self, rocket_position: tuple[float, float]):

        chunk_x = int((rocket_position[0] - (WIDTH - C_WIDTH) // 2) // C_WIDTH)
        chunk_y = int((-rocket_position[1] + (HEIGHT - C_HEIGHT) // 2) // C_HEIGHT)

        for x_offset in range(int(-self.load_x / 2), int(self.load_x / 2) + 1):
            for y_offset in range(int(-self.load_y / 2), int(self.load_y / 2) + 1):

                world_x = (WIDTH - C_WIDTH) // 2 + C_WIDTH * (x_offset + chunk_x)
                world_y = (HEIGHT - C_HEIGHT) // 2 + C_HEIGHT * (y_offset + chunk_y)

                chunk_screen_coordinates = world_to_screen_coordinates((world_x, -world_y), rocket_position, scale)

                # Draw the rectangles
                if chunk_y + y_offset >= -1:
                    background_color = (176, 235, 230 - (chunk_y + y_offset + 1) / 100)

                    pygame.draw.rect(screen, background_color, pygame.Rect(chunk_screen_coordinates[0], chunk_screen_coordinates[1], 
                                                                ceil(C_WIDTH * scale), ceil(C_HEIGHT * scale)))
                    pygame.draw.rect(screen, 'red', pygame.Rect(chunk_screen_coordinates[0], chunk_screen_coordinates[1], 
                                                                ceil(C_WIDTH * scale), ceil(C_HEIGHT * scale)), 1)


                # Draw the ground
                elif chunk_y + y_offset < -1:
                    pygame.draw.rect(screen, GROUND_COLOR, pygame.Rect(chunk_screen_coordinates[0], chunk_screen_coordinates[1], 
                                                                        ceil(C_WIDTH * scale), ceil(C_HEIGHT * scale)))
                
                # Create and find the size (length, height) of chunk text (mainly for debugging)
                chunk_coordinates_str = f"{chunk_x + x_offset} {chunk_y + y_offset}"
                chunk_coordinates_rendered = debug_font.render(chunk_coordinates_str, True, 'black', 'white')
                chunk_coordinates_str_size = debug_font.size(chunk_coordinates_str)
                chunk_coordinates_str_coordinates = world_to_screen_coordinates((WIDTH // 2 + C_WIDTH * (x_offset + chunk_x), -(HEIGHT // 2 + C_HEIGHT * (y_offset + chunk_y - 1))), rocket_position, scale)
                chunk_coordinates_str_coordinates = (chunk_coordinates_str_coordinates[0] - chunk_coordinates_str_size[0] / 2, chunk_coordinates_str_coordinates[1] - chunk_coordinates_str_size[1] / 2)

                # Write the chunk coordinates to the screen (uses basically the same equations like in background drawing)
                screen.blit(chunk_coordinates_rendered, chunk_coordinates_str_coordinates)

        # For debugging
        return (chunk_x, chunk_y)


def input():
    """ Keyboard input handling, acceleration and speed physics."""
    keys = pygame.key.get_pressed()

    # For debug fps changer
    global fps
    if keys[pygame.K_1]:
        fps = 30
    elif keys[pygame.K_2]:
        fps = 60
    elif keys[pygame.K_3]:
        fps = 120
    # Unlimited fps
    elif keys[pygame.K_4]:
        fps = 0
    elif keys[pygame.K_0]:
        fps = 1
    
    return keys



# Points on the corners of the rocket (size in px, coords origin is the center of the rocket)
collision_points = [[-25,50],[25,50],[-25,-50],[25,-50]]
#                 start_x,  start_y,    acceleration,
#                    |         |        |  boost acceleration,
#                    |         |        |  |   maximum speed
#                    |         |        |  |   |    points for collision
#                    |         |        |  |   |    |
rocket = Rocket(WIDTH / 2, HEIGHT / 2, 4, 8, 2000, collision_points, rocket_image_og)
background = Background(5,5)


first = True



# main loop
run = True

time1, time2 = 0,0

coin = PowerUp("money", 1, (400,0), coin_img)
cash = PowerUp("money", 2, (500,0), cash_img)
money_bag = PowerUp("money", 3, (600,0), money_bag_img)

powerups = [coin, cash, money_bag]

while run:
    # For FPS counter
    real_dt = (time.perf_counter_ns() - time1) / 1_000_000_000 # Because it is in nanoseconds
    time1 = time.perf_counter_ns()

    # Apply running fps and fill in the background
    dt = timer.tick(fps) * 0.001
    dt = 0.016

    # Fill the screen with background color
    screen.fill(SKY_COLOR)
    
    # Get input from keyboard mouse (HID)
    keys = input()

    # Update background
    chunk_coordinates = background.update(rocket.position)

    for powerup in powerups:
        powerup.draw(screen, scale, rocket.position)

    # Calculate new rocket position and draw the rocket
    speed = rocket.update(screen, dt, scale, keys)

    # Calculate the scale 
    scale = cubic_bezier(0, 0, 50, 0, 100, 100, 50, 100, speed / rocket.max_speed) / 100 + 1
    #pygame.draw.rect(screen, 'red', pygame.Rect(200, 200, 20, 20))
    # For debug info
    if not first:
        debug.info(screen, debug_font, rocket, last_speed, chunk_coordinates, scale, real_dt)
    else:
        first = False
    
    last_speed = rocket.x_speed, rocket.y_speed

    # Read HID inputs ONLY FOR QUITTING THE GAME
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Draw objects on the screen
    pygame.display.update()
    
pygame.quit()
            
    
        
