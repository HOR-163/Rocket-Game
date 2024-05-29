""" GOOD SOURCES FOR FUTURE """
# Gravity, physics: https://www.youtube.com/watch?v=5j0uU3aJxJM
# Camera control: https://www.youtube.com/watch?v=u7LPRqrzry8
# Collisions: https://www.youtube.com/watch?v=tJiKYMQJnYg
# Background scrolling/tiling: https://youtu.be/ARt6DLP38-Y

"""Start of the actual program"""
import pygame
from math import *
import sys
import time

# Extras
from CONSTANTS import *
from bezier_and_map import *
from coordinate_systems import *
from gameobjects import *
from collisions import check_collisions
from player import *
from gameobject_scripts import *
from background import *
from button import *

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

missing_texture = pygame.image.load(PATH + "/images/missing_texture.png").convert_alpha()

rocket_image = pygame.image.load(PATH + "/images/rocket2.png").convert_alpha()

coin_img = pygame.image.load(PATH + "/images/coin.png").convert_alpha()
cash_img = pygame.image.load(PATH + "/images/cash.png").convert_alpha()
money_bag_img = pygame.image.load(PATH + "/images/money_bag.png").convert_alpha()

small_fuel_img = pygame.image.load(PATH + "/images/small_fuel.png").convert_alpha()
medium_fuel_img = pygame.image.load(PATH + "/images/medium_fuel.png").convert_alpha()
large_fuel_img = pygame.image.load(PATH + "/images/large_fuel.png").convert_alpha()


cloud_image_0 = pygame.image.load(PATH + "/images/cloud0.png").convert_alpha() # Image width should be 150 or what looks good
cloud_image_1 = pygame.image.load(PATH + "/images/cloud1.png").convert_alpha() # Image width should be 175 or what looks good
cloud_image_2 = pygame.image.load(PATH + "/images/cloud2.png").convert_alpha() # Image width should be 200 or what looks good
cloud_image_3 = pygame.image.load(PATH + "/images/cloud3.png").convert_alpha() # Image width should be 250 or what looks good (or bigger)
cloud_image_4 = pygame.image.load(PATH + "/images/cloud4.png").convert_alpha() # Image width should be 300 or what looks good (or bigger)
cloud_image_5 = pygame.image.load(PATH + "/images/cloud5.png").convert_alpha() # Image width should be 400 or what looks good (or bigger)

ground = pygame.image.load(PATH + "/images/ground.png").convert_alpha()

# UI elements
wind_right = pygame.image.load(PATH + "/images/wind_right.png").convert_alpha()
wind_left = pygame.image.load(PATH + "/images/wind_left.png").convert_alpha()
danger = pygame.image.load(PATH + "/images/danger.png").convert_alpha()
BG = pygame.image.load(PATH + "/images/MenuBackground.png")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))



images = {1: coin_img, 2: cash_img, 3: money_bag_img,
          4: small_fuel_img, 5: medium_fuel_img, 6: large_fuel_img,
          # Obstacles
          "plane": missing_texture, "helicopter": missing_texture, "hot_air_balloon": missing_texture, "cloud": missing_texture, #level 1
          "fighter_jet": missing_texture,   # level 2
          "UFO": missing_texture, "satellite": missing_texture, #level 3
          None: missing_texture} 

times = []

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

""" wind_strength = 0
wind_duration = [2,4] # [x,y] aka x to y seconds
wind_timer = 0 """


""" # Points on the corners of the rocket (size in px, coords origin is the center of the rocket)
collision_points = [[-25,50],[25,50],[-25,-50],[25,-50]]
#                 start_x,  start_y,    acceleration,
#                    |         |        |  boost acceleration,
#                    |         |        |  |   maximum speed
#                    |         |        |  |   |    points for collision
#                    |         |        |  |   |    |
rocket = Rocket(WIDTH / 2, HEIGHT / 2, 4, 8, 2000, collision_points, rocket_image_og) """


# INITialize the objects
collision_points = [[1,49],[25,-1],[13,-50],[-11,-50], [-23,-1]]
#                 start_x,  start_y,    acceleration,
#                    |         |        |  boost acceleration,
#                    |         |        |  |   maximum speed
#                    |         |        |  |   |    start_fuel
#                    |         |        |  |   |    |           points for collision
#                    |         |        |  |   |    |           |                image
#                    |         |        |  |   |    |           |                |
rocket = Rocket((WIDTH / 2, HEIGHT / 2), 4, 8, 2000, 100, collision_points, rocket_image) # Rocket in gameobjects.py


player = Player(DEFAULT_PLAYER_DATA) # all of it in player.py
print(player.load_data())


background = Background(2 * CHUNK_GEN_RADIUS + 1, debug_font) # Background in background.py

minimap = MiniMap(player.minimap_radius) # Minimap in gameobjects.py

""" first = True 

run = True """

clouds = pygame.sprite.Group()
clouds.add(Cloud((random.randint(0, WIDTH),random.randint(0, HEIGHT)), cloud_image_0, 1.2))
clouds.add(Cloud((random.randint(0, WIDTH),random.randint(0, HEIGHT)), cloud_image_1, 1.15))
clouds.add(Cloud((random.randint(0, WIDTH),random.randint(0, HEIGHT)), cloud_image_2, 1.1))

clouds.add(Cloud((random.randint(0, WIDTH),random.randint(0, HEIGHT)), cloud_image_3, 1.05))
clouds.add(Cloud((random.randint(0, WIDTH),random.randint(0, HEIGHT)), cloud_image_4, 1.03))
clouds.add(Cloud((random.randint(0, WIDTH),random.randint(0, HEIGHT)), cloud_image_5, 1.01))



""" collision_debug_color = (0,0,0, 128)

# Used for debugging framerate and performance
time1, time2 = 0, 0
highest_dt = 0.0
dt = 0.016 """

def get_time():
    return time.perf_counter_ns()

def get_font(size):
    return pygame.font.Font(PATH + "/images/font.ttf", size)

def play():
    DEBUG = True
    scale = 1
    run = True
    first = True
    time1, time2 = 0,0
    highest_dt = 0.001
    dt = 0.16
    wind_timer = 0
    wind_strength = 0
    collision_group = pygame.sprite.Group()
    
    game_state = PLAYING
    chunk_coordinates = (0,-1)
    last_speed = (0,0)

    rocket.reset(player)

    while run:
        if game_state == PAUSED:
            keys = input()
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if keys[pygame.K_SPACE]:
                        game_state = PLAYING
                        break
                    elif keys[pygame.K_ESCAPE]:
                        player.save_data()
                        run = False
                        break
                elif event.type == pygame.QUIT:
                    player.save_data()
                    run = False
                    break
            timer.tick(fps)
            continue

        if first:
            create_objects_for_the_first_time(collision_group, images)
            screen.fill(SKY_COLOR)
            print(len(collision_group))

        # For FPS counter
        real_dt = (time.perf_counter_ns() - time1) / 1_000_000_000 # Because it is in nanoseconds

        if real_dt >= highest_dt and not first:
            highest_dt = real_dt
        time1 = time.perf_counter_ns()

        # pygame deltatime in ms
        dt = 0.016

        # Fill the screen with background color
        if not first:
            screen.fill(gradient(chunk_coordinates[1] + 2))

        # Get input from keyboard mouse (HID)
        keys = input()

        time12 = get_time()

        collided = check_collisions(player, rocket, collision_group, images)

        if collided:
            wind_strength = 0
            wind_timer = 0

        time13 = get_time()

        # Draw parallaxed clouds
        for cloud in clouds:
            cloud.draw(screen, rocket.screen_center, scale)

        # Update and draw background
        chunk_coordinates = background.update(screen, scale, rocket.screen_center ,ground, DEBUG)

        time14 = get_time()

        # Calculate new rocket position and draw the rocket
        rocket.update(screen, dt, scale, keys, player)
        rocket.draw(screen, scale)
        time15 = get_time()

        time16 = get_time()

        # Load and unload objects if they are too far from the rocket.
        objects_load_unload(collision_group, chunk_coordinates, images) # Located in gameobject_scripts.py

        time17 = get_time()
        
        minimap.draw_base(screen, rocket.position)

        time18 = get_time()



        # Go through all objects and move as well as draw them on the screen and on the minimap
        for object in collision_group:
            if object.type in MAGNETIC_OBJECTS:
                object.move_towards(rocket.position, rocket.speed, player, dt)

            object.update()
            object.draw(screen, scale, rocket.screen_center)
            
            # Draw all objects (fuel, money, obstacles) to the minimap
            minimap.draw(screen, rocket.position, object, DEBUG)
        

        time19 = get_time()

        # HERE GO ALL UI ELEMENTS
        money_and_fuel = debug_font.render(f"Money: {player.money} | Fuel: {round(rocket.fuel,0)}", True, 'black', 'white')
        screen.blit(money_and_fuel, (WIDTH // 2 - money_and_fuel.get_width() // 2, 0))

        if rocket.disabled > 0:
            if (rocket.disabled - int(rocket.disabled) < 0.5):
                    screen.blit(danger, (WIDTH / 2 - danger.get_width() / 2, HEIGHT / 2 - danger.get_height() / 2))

        if wind_timer == 0:
            wind_timer = (random.randint(0, WIND_CHANCE) == 1) * map_value(random.random(), 0,1, WIND_DURATION[0], WIND_DURATION[1])  # 4 seconds of wind
            if wind_timer != 0:
                wind_strength = random.randint(-10, 10)

        if wind_timer < 0:
            wind_timer = 0

        if wind_timer > 0:
            wind_timer -= dt
            rocket.angle += sin(radians(rocket.angle + 90)) * dt * wind_strength
            rocket.speed = (rocket.speed[0] + wind_strength * dt * 10, rocket.speed[1])
            if wind_strength < 0:
                wind_scaled_image = pygame.transform.scale_by(wind_right, scale)
                arrow_position = world_to_screen_coordinates(rocket.position, rocket.screen_center, scale)
                arrow_position = (arrow_position[0] + 75 * scale - wind_scaled_image.get_width() / 2, arrow_position[1] - wind_scaled_image.get_height() / 2)
                screen.blit(wind_scaled_image, arrow_position)
                
            if wind_strength > 0:
                wind_scaled_image = pygame.transform.scale_by(wind_left, scale)
                arrow_position = world_to_screen_coordinates(rocket.position, rocket.screen_center, scale)
                arrow_position = (arrow_position[0] -  75 * scale - wind_scaled_image.get_width() / 2, arrow_position[1] - wind_scaled_image.get_height() / 2)
                screen.blit(wind_scaled_image, arrow_position)


        time20 = get_time()

        # Calculate the scale 
        scale = cubic_bezier(0, 0, 50, 0, 100, 100, 50, 100, rocket.air_speed / rocket.max_speed) / 100 + 1

        time21 = get_time()

        # For debug info
        if not first and DEBUG == True:
            debug.info(screen, debug_font, rocket, last_speed, chunk_coordinates, scale, real_dt, highest_dt)
        else:
            first = False

        last_speed = rocket.speed

        # Read HID inputs ONLY FOR QUITTING THE GAME
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                run = False
                

            #Pressing the "R" key, resets the rocket
            if keys[pygame.K_r]:
                rocket.reset(player)
                wind_timer = 0
                wind_strength = 0

            if event.type == pygame.KEYUP:
                if keys[pygame.K_SPACE]:
                    game_state = PAUSED

                elif keys[pygame.K_F1]:
                    DEBUG = not DEBUG
                    rocket.debug = DEBUG

                elif keys[pygame.K_F2]:
                    print("------NEW------")
                    print("Fill and input: ", f"{time12 - time1:,}")
                    print("Check collisions: ", f"{time13 - time12:,}")
                    print("Update background: ", f"{time14 - time13:,}")
                    print("Update rocket: ", f"{time15 - time14:,}")
                    print("Get rocket_position: (probs smth small) ", f"{time16 - time15:,}")
                    print("Update objects: ", f"{time17 - time16:,}")
                    print("Draw minimap base: ", f"{time18 - time17:,}")
                    print("Object movement and minimap draw: ", f"{time19 - time18:,}")
                    print("Money and fuel display: ",  f"{time20 - time19:,}")
                    print("Scale calculation: ", f"{time21 - time20:,}")
                    print("debug settings and display.update():", f"{time22 - time21:,}")
                    times.append([time12 - time1, time13 - time12, time14 - time13, time15 - time14, time16 - time15, time17 - time16, time18 - time17, time19 - time18, time20 - time19, time21 - time20])
                    averages = [0 for _ in range(len(times[0]) + 1)]
                    for x in times:
                        for index, y in enumerate(x):
                            averages[index] += y
                        averages[-1] += sum(x)
                    for x in range(len(averages)):
                        averages[x] = averages[x] / len(times)
                    print("Averages:", {y: f"{int(x):,}" for y,x in enumerate(averages)}, "| Count:", len(times))
                    #print([time12 - time1, time13 - time12, time14 - time13, time15 - time14, time16 - time15, time17 - time16, time18 - time17, time19 - time18, time20 - time19, time21 - time20, time22 - time21])




        # Update the screen
        pygame.display.update()

        time22 = get_time()

        # Apply running fps
        dt = timer.tick(fps) * 0.001

def upgrades():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")

        UPGRADES_TEXT = get_font(45).render("UPGRADES", True, "Black")
        UPGRADES_RECT = UPGRADES_TEXT.get_rect(center=(WIDTH/2, HEIGHT/3))
        screen.blit(UPGRADES_TEXT, UPGRADES_RECT)

        UPGRADES_BACK = Button(image=None, pos=(WIDTH/2, HEIGHT/1.5), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        UPGRADES_BACK.changeColor(OPTIONS_MOUSE_POS)
        UPGRADES_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if UPGRADES_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("ROCKETMAN", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(500, 100))

        # All avaliable buttons on the screen
        PLAY_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(500, 250), 
                            text_input="PLAY", font=get_font(70), base_color="#d7fcd4", hovering_color="White")
        UPGRADES_BUTTON = Button(image=pygame.image.load("images/Upgrades Rect.png"), pos=(500, 400), 
                            text_input="UPGRADES", font=get_font(70), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("images/Quit Rect.png"), pos=(500, 550), 
                            text_input="QUIT", font=get_font(70), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, UPGRADES_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        # If a button is pressed, starts any of the options (game, upgrades, quit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if UPGRADES_BUTTON.checkForInput(MENU_MOUSE_POS):
                    upgrades()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        timer.tick(fps)

main_menu()

    
#pygame.quit()
            
    
        
