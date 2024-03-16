""" GOOD SOURCES FOR FUTURE """
# Gravity, physics: https://www.youtube.com/watch?v=5j0uU3aJxJM
# Camera control: https://www.youtube.com/watch?v=u7LPRqrzry8
# Collisions: https://www.youtube.com/watch?v=tJiKYMQJnYg
# Background scrolling/tiling: https://youtu.be/ARt6DLP38-Y

"""Start of the actual program"""
import pygame
import math
import os
import time

#Initialize the pygame module and attributes that are related to it
pygame.init()
# Screen size
WIDTH = 1000
HEIGHT = 750
# Size of background chunks
C_WIDTH = WIDTH / 2
C_HEIGHT = HEIGHT / 2

# Initialize the game
screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption("Rocket Game beta")
fps = 60
timer = pygame.time.Clock()

GROUND_COLOR = (224, 173, 52)
SKY_COLOR = (176, 235, 230)

# load the rocket image
path = os.getcwd()
# For IDLE uncomment the following line (in VSCode comment this line)
#path = path[:path.rfind("\\") + 1] # <------- This one
rocket_image_og = pygame.image.load(path + "\\images\\rocket1.png").convert_alpha()

# Set some global variables for the rockets
gravity = 4
max_falling_speed = 600
scale = 1

#Define the debug font
debug_font = pygame.font.SysFont('consolas', 15)


class Rocket:
    def __init__(self, x_pos, y_pos, acceleration, boost, max_speed):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.acceleration = acceleration
        self.boost = boost
        self.max_speed = max_speed
        self.angle = 0
        self.x_speed = 0
        self.y_speed = 0
        
    """ Keyboard input handling and accelerationa and speed physics """
    def input(self):
        keys = pygame.key.get_pressed()

        # Pressing up so add boost
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.x_speed += math.cos(math.radians(self.angle - 90)) * self.boost
            self.y_speed += math.sin(math.radians(self.angle - 90)) * self.boost
        # Pressing down, so no acceleration
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.y_speed <= max_falling_speed:
            self.y_speed += gravity
        # Pressing nothing, so we have to add acceleration
        else:
            self.x_speed += math.cos(math.radians(self.angle - 90)) * self.acceleration
            self.y_speed += math.sin(math.radians(self.angle - 90)) * self.acceleration
            
        
        # Pressing right, so rotate rocket clockwise
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle -= 20 * fps_dt / 1000000000
        # Pressing left, so rotate rocket counter-clockwise
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle += 20 * fps_dt / 1000000000
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
            scale += 0.2 * fps_dt / 1000000000
        elif keys[pygame.K_q]:
            if scale >= 0.1:
                scale -= 0.2 * fps_dt / 1000000000

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


            

    """ Update the rockets position """
    def update(self):
        # Read keyboard inputs, calculate speeds
        self.input()

        # Limit the speeds to be in range of maximum speed
        air_speed = math.sqrt(self.x_speed ** 2 + self.y_speed ** 2)
        if air_speed > self.max_speed:
            self.x_speed = self.max_speed / air_speed * self.x_speed
            self.y_speed = self.max_speed / air_speed * self.y_speed
        
        self.x_pos -= self.x_speed * fps_dt / 1000000000
        self.y_pos += self.y_speed * fps_dt / 1000000000

        # Put the image in the centre of our imaginary "position point" aka when rotating the rocket
        # it rotates from the center, not from the upper left corner of the image (sprite)
        # Always draw the rocket in the center of the screen (maybe change later)
        # Also apply scale to the rocket
        img_x = WIDTH / 2 + self.x_speed / self.max_speed * WIDTH / 5
        img_y = HEIGHT / 2 - self.y_speed / self.max_speed * HEIGHT / 5

        rocket_image_scaled = pygame.transform.scale(rocket_image_og, (50 * scale, 100 * scale))
        rocket_image_scaled_and_rotated = pygame.transform.rotate(rocket_image_scaled, self.angle)
        rocket_image_rect = rocket_image_scaled_and_rotated.get_rect(center = (img_x, img_y))
        screen.blit(rocket_image_scaled_and_rotated, rocket_image_rect)
        #pygame.draw.circle(screen, 'red', (WIDTH // 2, HEIGHT // 2), 1) # To find the center of the screen
        return air_speed

"""Handle background chunks"""
class Background:
    def __init__(self, load_x: int, load_y: int):
        # how many chunks to load (e.g 3x3 amount of chunks)
        self.load_x = load_x
        self.load_y = load_y
        
    def update(self, x_pos, y_pos):
        chunk_x = int((x_pos - (WIDTH - C_WIDTH) / 2) // C_WIDTH)
        chunk_y = int((-y_pos + (HEIGHT - C_HEIGHT) / 2) // C_HEIGHT + 1)


        for x_offset in range(int(-self.load_x / 2), int(self.load_x / 2) + 1):
            for y_offset in range(int(-self.load_y / 2), int(self.load_y / 2) + 1):
                # Find the center origin of scale
                center_x = ((WIDTH - C_WIDTH) * scale + WIDTH) / 2
                center_y = ((HEIGHT - C_HEIGHT) * scale + HEIGHT) / 2

                # Draw the rectangles
                pygame.draw.rect(screen, 'red', pygame.Rect(
                    (-x_pos + (chunk_x + x_offset) * C_WIDTH) * scale + center_x, 
                    (-y_pos - (chunk_y + y_offset) * C_HEIGHT) * scale + center_y, 
                    math.ceil(C_WIDTH * scale), math.ceil(C_HEIGHT * scale)), 1) # Has to be ceil, otherwise seams will appear

                # Draw the gorund
                if chunk_y + y_offset < 0:
                    pygame.draw.rect(screen, GROUND_COLOR , pygame.Rect(
                    (-x_pos + (chunk_x + x_offset) * C_WIDTH) * scale + center_x, 
                    (-y_pos - (chunk_y + y_offset) * C_HEIGHT) * scale + center_y, 
                    math.ceil(C_WIDTH * scale), math.ceil(C_HEIGHT * scale))) # Has to be ceil, otherwise seams will appear
                
                # Create and find the size (length, height) of chunk text (mainly for debugging)
                coord_text = f"{chunk_x + x_offset} {chunk_y + y_offset}"
                coord_text_font_object = debug_font.render(coord_text, True, 'black', 'white')
                coord_text_size_x, coord_text_size_y = debug_font.size(coord_text)

                # Write the chunk coordinates to the screen (uses basically the same equations like in background drawing)
                screen.blit(coord_text_font_object, ((-x_pos + C_WIDTH / 2 + (chunk_x + x_offset) * C_WIDTH) * scale + center_x - coord_text_size_x / 2, 
                                            (-y_pos  + C_HEIGHT / 2 - (chunk_y + y_offset) * C_HEIGHT) * scale + center_y - coord_text_size_y / 2))
        # For debugging
        return [chunk_x, chunk_y]



#                 start_x,  start_y,    acceleration,
#                    |         |        |  boost acceleration,
#                    |         |        |  |   maximum speed
#                    |         |        |  |   |
rocket1 = Rocket(WIDTH / 2, HEIGHT / 2, 4, 8, 2000)
background = Background(5,5)


first = True
def print_debug_info(last_speed_x, last_speed_y, chunk_x, chunk_y):
    x_position = round(rocket1.x_pos, 3)
    y_position = round(rocket1.y_pos, 3)
    x_speed = round(rocket1.x_speed, 3)
    y_speed = round(rocket1.y_speed, 3)
    x_acc = round((x_speed - last_speed_x), 3)
    y_acc = round((y_speed - last_speed_y), 3)
    angle = round(rocket1.angle, 3)
    texts = [debug_font.render(f"x-position: {x_position}", True, 'red', 'white'),
             debug_font.render(f"y-position: {y_position}", True, 'blue', 'white'),
             debug_font.render(f"Chunk based position: {chunk_x} {chunk_y}", True, 'black', 'white'),
             debug_font.render(f"x-speed: {-x_speed}", True, 'red', 'white'),
             debug_font.render(f"y-speed: {-y_speed}", True, 'blue', 'white'),
             debug_font.render(f"Actual speed: {round(math.sqrt(x_speed ** 2 + y_speed ** 2),3)}", True, 'black', 'white'),
             debug_font.render(f"x-acceleration: {-x_acc}", True, 'red', 'white'),
             debug_font.render(f"y-acceleration: {-y_acc}", True, 'blue', 'white'),
             debug_font.render(f"Angle: {-angle}", True, 'red', 'white'),
             debug_font.render(f"Scale: {round(scale, 2)}", True, 'black', 'white'),
             debug_font.render(f"FPS: {round(1000000000/(fps_dt), 3)}", True, 'black', 'white')
             ]
    for index, text in enumerate(texts):
        screen.blit(text, (0, index * 16))

# main loop
run = True

time1, time2 = 0,0
fps_dt = 160000000
times = []

while run:
    # For FPS counter
    times.append(time2 - time1)
    if len(times) == 5:
        fps_dt = sum(times) / 5
        times = []
    time1 = time.perf_counter_ns()

    # Apply running fps and fill in the background
    dt = timer.tick(fps) * 0.001
    screen.fill(SKY_COLOR)

    # Update background
    chunk_coord = background.update(rocket1.x_pos, rocket1.y_pos)
    # Read hid input and calculate some values
    speed = rocket1.update()

    scale = 1 / (0.5 * (speed / rocket1.max_speed) ** 5 + 0.5 * (speed / rocket1.max_speed) ** 3  + 0.1 * speed / rocket1.max_speed + 1)
    print(scale)

    # Read hid inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # For debug info
    if not first:
        print_debug_info(last_speed_x, last_speed_y, chunk_coord[0], chunk_coord[1])
    first = False
    last_speed_x, last_speed_y = rocket1.x_speed, rocket1.y_speed

    # Draw things on the screen
    pygame.display.flip()

    # For FPS counter
    time2 = time.perf_counter_ns()
pygame.quit()
            
    
        
