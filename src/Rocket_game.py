# Gravity, physics: https://www.youtube.com/watch?v=5j0uU3aJxJM
# Camera control: https://www.youtube.com/watch?v=u7LPRqrzry8
# Collisions: https://www.youtube.com/watch?v=tJiKYMQJnYg

import pygame, math, os
import time

#Initialize the pygame module
pygame.init()
WIDTH = 1000
HEIGHT = 750
screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption("Rocket Game v0.001")
fps = 60
timer = pygame.time.Clock()


# load the rocket image
path = os.getcwd()
#For IDLE
path = path[:path.rfind("\\") + 1]
rocket_image_og = pygame.image.load(path + "\\images\\rocket1.png").convert_alpha()

# Set some global variables for the rockets
gravity = 0.2
max_falling_speed = 10

# Just some random stuff
background_color = (176, 235, 230)
font = pygame.font.SysFont('consolas', 15)


class Rocket:
    def __init__(self, x_pos, y_pos, acceleration, boost, id):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.acceleration = acceleration
        self.boost = boost
        self.id = id
        self.angle = 0
        self.x_speed = 0
        self.y_speed = 0
        

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
            self.angle -= 0.5
        # Pressing left, so rotate rocket counter-clockwise
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle += 0.5

        #Pressing the "R" key, resets everything
        if keys[pygame.K_r]:
            self.x_pos = 500
            self.y_pos = 375
            self.x_speed = 0
            self.y_speed = 0
            self.angle = 0
        
    def update(self):
        self.input()
        self.x_pos -= self.x_speed
        self.y_pos += self.y_speed

        # Put the image in the centre of our imaginary "position point" aka when rotating the rocket
        # it rotates from the center, not form the upper left corenr of the image (sprite)
        rocket_image = pygame.transform.rotate(rocket_image_og, self.angle)
        rocket_image_rect = rocket_image.get_rect(center = (self.x_pos, self.y_pos))
        screen.blit(rocket_image, rocket_image_rect)


rocket1 = Rocket(500, 375, 0.1, 0.2, 1)



first = True
def print_debug_info(last_speed_x, last_speed_y):
    x_position = round(rocket1.x_pos - 500, 3)
    y_position = round(-rocket1.y_pos + 375, 3)
    x_speed = round(rocket1.x_speed, 3)
    y_speed = round(rocket1.y_speed, 3)
    x_acc = round((x_speed - last_speed_x), 3)
    y_acc = round((y_speed - last_speed_y), 3)
    angle = round(rocket1.angle, 3)
    texts = [font.render(f"x-position: {x_position}", True, 'red', 'white'),
             font.render(f"y-position: {y_position}", True, 'blue', 'white'),
             font.render(f"x-speed: {-x_speed}", True, 'red', 'white'),
             font.render(f"y-speed: {-y_speed}", True, 'blue', 'white'),
             font.render(f"Actual speed: {round(math.sqrt(x_speed**2 + y_speed**2),3)}", True, 'black', 'white'),
             font.render(f"x-acceleration: {-x_acc}", True, 'red', 'white'),
             font.render(f"y-acceleration: {-y_acc}", True, 'blue', 'white'),
             font.render(f"Angle: {-angle}", True, 'red', 'white'),
             font.render(f"FPS: {round(1000000000/(deltatime), 3)}", True, 'black', 'white')
             ]
    for index, text in enumerate(texts):
        screen.blit(text,(0,index * 16))



# main loop
run = True

time1, time2 = 0,0
deltatime = 160000000
times = []

while run:
    # For FPS counter
    times.append(time2 - time1)
    if len(times) == 5:
        deltatime = sum(times) / 5
        times = []
    time1 = time.perf_counter_ns()

    # Apply running fps and fill in the background
    timer.tick(fps)
    screen.fill(background_color)

    # Run the main code in the rocket object
    rocket1.update()

    # Read hid inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # For debug info
    if not first:
        print_debug_info(last_speed_x, last_speed_y)
    first = False
    last_speed_x, last_speed_y = rocket1.x_speed, rocket1.y_speed

    # Draw things on the screen
    pygame.display.flip()

    # For FPS counter
    time2 = time.perf_counter_ns()
pygame.quit()
            
    
        
