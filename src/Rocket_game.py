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

#Initialize the pygame module and attributes that are related to it
pygame.init()

# Initialize the game
screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption("Rocket Game beta")
fps = 60
timer = pygame.time.Clock()

# load the rocket image
path = os.getcwd()
# For IDLE uncomment the following line (in VSCode comment this line)
#path = path[:path.rfind("\\") + 1] # <------- This one
rocket_image_og = pygame.image.load(path + "\\images\\rocket1.png").convert_alpha()

# Set some global variables for the rockets
scale = 1

#Define the debug font
debug_font = pygame.font.SysFont('consolas', 15)

class CollisionPoint:
    def __init__(self, coordinates: list):
        self.x_offset = coordinates[0]
        self.y_offset = coordinates[1]
        self.x_pos = 0
        self.y_pos = 0
        self.radius = sqrt(pow(coordinates[0], 2) + pow(coordinates[1], 2))
    
    @property
    def screen_position(self) -> tuple[float, float]:
        return (self.x_pos, self.y_pos)

    def update(self, angle: float, screen_x_offset: int, screen_y_offset: int) -> tuple[float, float]:
        angle = radians(angle) + atan2(self.y_offset, self.x_offset)
        self.x_pos = screen_x_offset + self.radius * cos(angle) * scale
        self.y_pos = screen_y_offset - self.radius * sin(angle) * scale
        return self.screen_position
    

class Rocket:
    def __init__(self, x_pos, y_pos, acceleration, boost, max_speed, collision_points):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.acceleration = acceleration
        self.boost = boost
        self.max_speed = max_speed
        self.angle = 0
        self.x_speed = 0
        self.y_speed = 0
        self.collision_points = []
        for point in collision_points:
            self.collision_points.append(CollisionPoint(point))

    def input(self):
        """ Keyboard input handling, acceleration and speed physics."""
        keys = pygame.key.get_pressed()

        # Pressing up so add boost
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.x_speed += cos(radians(self.angle - 90)) * self.boost
            self.y_speed += sin(radians(self.angle - 90)) * self.boost
        # Pressing down, so no acceleration
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.y_speed <= FALL_SPEED:
            self.y_speed += GRAVITY
        # Pressing nothing, so we have to add acceleration
        else:
            self.x_speed += cos(radians(self.angle - 90)) * self.acceleration
            self.y_speed += sin(radians(self.angle - 90)) * self.acceleration
            
        
        # Pressing right, so rotate rocket clockwise
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle -= 20 * dt
        # Pressing left, so rotate rocket counter-clockwise
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle += 20 * dt
        global scale
        #Pressing the "R" key, resets everything
        if keys[pygame.K_r]:
            self.x_pos = WIDTH / 2
            self.y_pos = HEIGHT / 2
            self.x_speed = 0
            self.y_speed = 0
            self.angle = 0
            scale = 1

        # For debug scaling
        if keys[pygame.K_e]:
            scale += 0.2 * dt
        elif keys[pygame.K_q]:
            if scale >= 0.1:
                scale -= 0.2 * dt

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

    def update(self):
        """ Update the rockets position."""
        # Read keyboard inputs, calculate speeds
        self.input()

        # Limit the speeds to be in range of maximum speed
        air_speed = sqrt(self.x_speed ** 2 + self.y_speed ** 2)
        if air_speed > self.max_speed:
            self.x_speed = self.max_speed / air_speed * self.x_speed
            self.y_speed = self.max_speed / air_speed * self.y_speed
        
        self.x_pos -= self.x_speed * dt
        self.y_pos += self.y_speed * dt


        # Put the image in the center of our imaginary "position point" aka when rotating the rocket
        # it rotates from the center, not from the upper left corner of the image (sprite)
        # Also apply scale to the rocket

        img_width = rocket_image_og.get_width()
        img_height = rocket_image_og.get_height()

        x_img_offset = cubic_bezier(0,0,50,0,50,100,100,100, self.x_speed / self.max_speed) #,screen, position=(WIDTH - 100, HEIGHT - 100))
        y_img_offset = cubic_bezier(0,0,50,0,50,100,100,100, self.y_speed / self.max_speed) #,screen, color='blue',position=(WIDTH - 100, HEIGHT- 200))
        img_x = WIDTH / 2 - x_img_offset * WIDTH / (2 * 100)
        img_y = HEIGHT / 2 + y_img_offset * HEIGHT / (2 * 100)

        # print(x_offset_amount, y_offset_amount)

        lowest = None
        for index, point in enumerate(self.collision_points):
            pygame.draw.circle(screen, COLORS[index % 8], point.update(self.angle, img_x, img_y), 2)
            point_y_position = point.screen_position[1]
            if lowest is None or lowest.screen_position[1] < point_y_position:
                lowest = point

        # If the lowest point intersects with ground
        if screen_to_world_coordinates((None, lowest.screen_position[1]), self.position, scale)[1] > HEIGHT / 2 + C_HEIGHT / 2:
            pygame.draw.circle(screen, "green", lowest.screen_position, 5)
            self.y_pos += (world_to_screen_coordinates((None, HEIGHT / 2 + C_HEIGHT / 2 + 2), self.position, scale)[1] - lowest.screen_position[1])
            self.x_speed = self.x_speed - self.x_speed * GROUND_FRICTION
            self.y_speed = 0 

        """ if -(HEIGHT - self.y_pos - lowest[0].screen_position[1]) >= C_HEIGHT/ 2:
            pygame.draw.circle(screen, "red", lowest[0].screen_position, 3)
            #print(HEIGHT + C_HEIGHT / 2 - self.y_pos - lowest[0].screen_position[1])
            self.y_pos += HEIGHT + C_HEIGHT / 2 - self.y_pos - lowest[0].screen_position[1]
            self.x_speed = self.x_speed - self.x_speed / 100
            self.y_speed = 0 """

        pygame.draw.circle(screen, "white", (img_x, img_y), 2)
        
        rocket_image_scaled = pygame.transform.scale(rocket_image_og, (img_width * scale, img_height * scale))
        rocket_image_scaled_and_rotated = pygame.transform.rotate(rocket_image_scaled, self.angle)
        rocket_image_rect = rocket_image_scaled_and_rotated.get_rect(center = (img_x, img_y))
        screen.blit(rocket_image_scaled_and_rotated, rocket_image_rect)

        #pygame.draw.circle(screen, 'red', (WIDTH // 2, HEIGHT // 2), 1) # To find the center of the screen
        return air_speed

    @property
    def position(self):
        return (self.x_pos, self.y_pos)
    

"""Handle background"""
class Background:
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
                    pygame.draw.rect(screen, 'red', pygame.Rect(chunk_screen_coordinates[0], chunk_screen_coordinates[1], 
                                                                ceil(C_WIDTH * scale), ceil(C_HEIGHT * scale)), 1)

                # Draw the ground
                elif chunk_y + y_offset < -1:
                    pygame.draw.rect(screen, GROUND_COLOR , pygame.Rect(chunk_screen_coordinates[0], chunk_screen_coordinates[1], 
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





# Points on the corners of the rocket (size in px, coords origin is the center of the rocket)
collision_points = [[-25,50],[25,50],[-25,-50],[25,-50]]
#                 start_x,  start_y,    acceleration,
#                    |         |        |  boost acceleration,
#                    |         |        |  |   maximum speed
#                    |         |        |  |   |    points for collision
#                    |         |        |  |   |    |
rocket1 = Rocket(WIDTH / 2, HEIGHT / 2, 4, 8, 2000, collision_points)
background = Background(5,5)


first = True
def print_debug_info(last_speed, chunk_coordinates):
    x_position = round(rocket1.position[0], 3)
    y_position = round(rocket1.position[1], 3)
    x_speed = round(rocket1.x_speed, 3)
    y_speed = round(rocket1.y_speed, 3)
    x_acc = round((x_speed - last_speed[0]), 3)
    y_acc = round((y_speed - last_speed[1]), 3)
    angle = round(rocket1.angle, 3)
    texts = [debug_font.render(f"x-position: {x_position}", True, 'red', 'white'),
             debug_font.render(f"y-position: {y_position}", True, 'blue', 'white'),
             debug_font.render(f"Chunk based position: {chunk_coordinates[0]} {chunk_coordinates[1]}", True, 'black', 'white'),
             debug_font.render(f"x-speed: {-x_speed}", True, 'red', 'white'),
             debug_font.render(f"y-speed: {-y_speed}", True, 'blue', 'white'),
             debug_font.render(f"Actual speed: {round(sqrt(x_speed ** 2 + y_speed ** 2),3)}", True, 'black', 'white'),
             debug_font.render(f"x-acceleration: {-x_acc}", True, 'red', 'white'),
             debug_font.render(f"y-acceleration: {-y_acc}", True, 'blue', 'white'),
             debug_font.render(f"Angle: {-angle}", True, 'red', 'white'),
             debug_font.render(f"Scale: {round(scale, 2)}", True, 'black', 'white'),
             debug_font.render(f"FPS: {round(1/(dt), 3)}", True, 'black', 'white')
             ]
    for index, text in enumerate(texts):
        screen.blit(text, (0, index * 16))


# main loop
run = True

time1, time2 = 0,0

while run:
    # For FPS counter
    dt = (time.perf_counter_ns() - time1) / 1_000_000_000 # Because it is in nanoseconds
    time1 = time.perf_counter_ns()

    # Apply running fps and fill in the background
    dt = timer.tick(fps) * 0.001
    dt = 0.016

    # Fill the screen with background color
    screen.fill(SKY_COLOR)
    
    # Update background
    chunk_coordinates = background.update(rocket1.position)

    # Read hid input and calculate some values
    speed = rocket1.update()

    # Calculate the scale 
    scale = cubic_bezier(0, 0, 50, 0, 100, 100, 50, 100, speed / rocket1.max_speed) / 100 + 1

    # Read hid inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # For debug info
    if not first:
        print_debug_info(last_speed, chunk_coordinates)
    first = False
    last_speed = rocket1.x_speed, rocket1.y_speed

    # Draw things on the screen
    pygame.display.update()
pygame.quit()
            
    
        
