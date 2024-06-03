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
from ui_elements import *

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

# Progress bar with steps
right_arrow_default = pygame.image.load(PATH + "/images/right_arrow_default.png").convert_alpha()
right_arrow_hover = pygame.image.load(PATH + "/images/right_arrow_hover.png").convert_alpha()
left_arrow_default = pygame.image.load(PATH + "/images/left_arrow_default.png").convert_alpha()
left_arrow_hover = pygame.image.load(PATH + "/images/left_arrow_hover.png").convert_alpha()

BG = pygame.image.load(PATH + "/images/MenuBackground.png")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

bg_col = (0,0,0,128)

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

# HAS TO ALWAYS BE HERE, SO THAT ALL FUNCTION (PLAY, UPGRADE, ...) CAN REACH IT
player = Player(DEFAULT_PLAYER_DATA) # all of it in player.py


def get_time():
    return time.perf_counter_ns()

def get_font(size):
    return pygame.font.Font(PATH + "/images/font.ttf", size)

def draw_ui(rocket, wind_strength, scale):
    money_and_fuel = debug_font.render(f"Money: {player.money} | Fuel: {round(rocket.fuel,0)}", True, 'black', 'white')
    screen.blit(money_and_fuel, (WIDTH // 2 - money_and_fuel.get_width() // 2, 0))

    if rocket.disabled > 0:
        if (rocket.disabled - int(rocket.disabled) < 0.5):
                screen.blit(danger, (WIDTH / 2 - danger.get_width() / 2, HEIGHT / 2 - danger.get_height() / 2))

        
    if wind_strength < 0:
        wind_scaled_image = pygame.transform.scale_by(wind_right, scale)
        arrow_position = world_to_screen_coordinates(rocket.position, rocket.screen_center, scale)
        arrow_position = (arrow_position[0] - 75 * scale - wind_scaled_image.get_width() / 2, arrow_position[1] - wind_scaled_image.get_height() / 2)
        screen.blit(wind_scaled_image, arrow_position)
        
    if wind_strength > 0:
        wind_scaled_image = pygame.transform.scale_by(wind_left, scale)
        arrow_position = world_to_screen_coordinates(rocket.position, rocket.screen_center, scale)
        arrow_position = (arrow_position[0] +  75 * scale - wind_scaled_image.get_width() / 2, arrow_position[1] - wind_scaled_image.get_height() / 2)
        screen.blit(wind_scaled_image, arrow_position)

def pause_menu(rocket, background, minimap,chunk_coordinates, collision_group, clouds, wind_strength, scale):
    keys = input()
    game_state = PAUSED
    run = True
    
    screen.fill(gradient(chunk_coordinates[1] + 2))

    background.update(screen, scale, rocket.position, ground)

    for cloud in clouds:
        cloud.draw(screen, rocket.screen_center, scale)

    rocket.draw(screen, scale)
    if player.map_level > 0:
        minimap.draw_base(screen, rocket.position)

    for object in collision_group:
        object.draw(screen, rocket.screen_center, scale)
        if player.map_level > 0:
            minimap.draw(screen, rocket.position, object)

    draw_ui(rocket, wind_strength, scale)

    draw_rect_alpha(screen, (0,0,0,50), pygame.Rect(0,0,WIDTH, HEIGHT))

    MOUSE_POS = pygame.mouse.get_pos()

    MENU_TEXT = get_font(100).render("PAUSED", True, TEXT_HEADER_COLOR)
    MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2, 100))

    # All avaliable buttons on the screen
    CONTINUE_BUTTON = Button((WIDTH / 2, 250), "CONTINUE", get_font(70), TEXT_DEFAULT_COLOR, TEXT_HOVER_COLOR, bg_color = TEXT_BACKGROUND_COLOR)
    RESTART_BUTTON = Button((WIDTH / 2, 400), "RESTART", get_font(70), TEXT_DEFAULT_COLOR, TEXT_HOVER_COLOR, bg_color = TEXT_BACKGROUND_COLOR)
    MAIN_MENU_BUTTON = Button((WIDTH / 2, 550), "MAIN MENU", get_font(70), TEXT_DEFAULT_COLOR, TEXT_HOVER_COLOR, bg_color = TEXT_BACKGROUND_COLOR)

    screen.blit(MENU_TEXT, MENU_RECT)

    for button in [CONTINUE_BUTTON, RESTART_BUTTON, MAIN_MENU_BUTTON]:
        button.changeColor(MOUSE_POS)
        button.update(screen)

    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if keys[pygame.K_SPACE]:
                game_state = PLAYING
                break
            elif keys[pygame.K_ESCAPE]:
                player.save_data()
                run = False
                break
        if event.type == pygame.QUIT:
            player.save_data()
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if CONTINUE_BUTTON.checkForInput(MOUSE_POS):
                game_state = PLAYING
                break
            if RESTART_BUTTON.checkForInput(MOUSE_POS):
                player.save_data()
                rocket.reset(player)
                reset_objects(collision_group, images)
                wind_strength = 0
                game_state = PLAYING
                break
            if MAIN_MENU_BUTTON.checkForInput(MOUSE_POS):
                player.save_data()
                run = False
                break


    pygame.display.update()
    timer.tick(fps)

    return game_state, run
    

def play():

    print(player.load_data())

    # INITialize the objects
    collision_points = [[1,49],[25,-1],[13,-50],[-11,-50], [-23,-1]]

    max_speed = player.starting_speed + player.max_speed_level * ROCKET_SPEED_MULTIPLIER
    start_fuel = player.starting_fuel + player.fuel_level * FUEL_LEVEL_MULTIPLIER
    #                 start_x,  start_y,     acceleration,
    #                    |         |         |   boost acceleration,
    #                    |         |         |   |   maximum speed
    #                    |         |         |   |   |          start_fuel
    #                    |         |         |   |   |          |           points for collision
    #                    |         |         |   |   |          |           |                image
    #                    |         |         |   |   |          |           |                |
    rocket = Rocket((WIDTH / 2, HEIGHT / 2), 4, 8, max_speed, start_fuel, collision_points, rocket_image) # Rocket in gameobjects.py

    


    background = Background(2 * CHUNK_GEN_RADIUS + 1, debug_font) # Background in background.py

    minimap = MiniMap(player.map_level) # Minimap in gameobjects.py

    clouds = pygame.sprite.Group()
    clouds.add(Cloud((random.randint(0, WIDTH),random.randint(0, HEIGHT)), cloud_image_0, 1.2))
    clouds.add(Cloud((random.randint(0, WIDTH),random.randint(0, HEIGHT)), cloud_image_1, 1.15))
    clouds.add(Cloud((random.randint(0, WIDTH),random.randint(0, HEIGHT)), cloud_image_2, 1.1))

    clouds.add(Cloud((random.randint(0, WIDTH),random.randint(0, HEIGHT)), cloud_image_3, 1.05))
    clouds.add(Cloud((random.randint(0, WIDTH),random.randint(0, HEIGHT)), cloud_image_4, 1.03))
    clouds.add(Cloud((random.randint(0, WIDTH),random.randint(0, HEIGHT)), cloud_image_5, 1.01))


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
            game_state, run = pause_menu(rocket, background, minimap, chunk_coordinates, collision_group, clouds, wind_strength, scale)
            continue

        if first:
            create_objects_for_the_first_time(collision_group, images)
            screen.fill(SKY_COLOR)

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

        collided = check_collisions(player, rocket, collision_group, images)

        if collided:
            wind_strength = 0
            wind_timer = 0

        # Draw parallaxed clouds
        for cloud in clouds:
            cloud.draw(screen, rocket.screen_center, scale)

        # Update and draw background
        chunk_coordinates = background.update(screen, scale, rocket.screen_center ,ground, DEBUG)

        # Calculate new rocket position and draw the rocket
        rocket.update(screen, dt, scale, keys, player)
        rocket.draw(screen, scale)

        # Load and unload objects if they are too far from the rocket.
        objects_load_unload(collision_group, chunk_coordinates, images) # Located in gameobject_scripts.py

        if player.map_level > 0:
            minimap.draw_base(screen, rocket.position)

        # Go through all objects and move as well as draw them on the screen and on the minimap
        for object in collision_group:
            if object.type in MAGNETIC_OBJECTS:
                object.move_towards(rocket.position, rocket.speed, player, dt)

            object.update()
            object.draw(screen, rocket.screen_center, scale)
            
            # Draw all objects (fuel, money, obstacles) to the minimap
            if player.map_level > 0:
                minimap.draw(screen, rocket.position, object, DEBUG)

        if wind_timer == 0:
            wind_timer = (random.randint(0, WIND_CHANCE) == 1) * map_value(random.random(), 0,1, WIND_DURATION[0], WIND_DURATION[1])  # 4 seconds of wind
            if wind_timer != 0:
                wind_strength = random.randint(-10, 10)

        if wind_timer < 0:
            wind_timer = 0

        wind_timer -= dt
        rocket.angle += sin(radians(rocket.angle + 90)) * dt * wind_strength
        rocket.speed = (rocket.speed[0] + wind_strength * dt * 10, rocket.speed[1])

        # HERE GO ALL UI ELEMENTS
        draw_ui(rocket, wind_strength, scale)

        # Calculate the scale 
        #scale = cubic_bezier(0, 0, 50, 0, 100, 100, 50, 100, rocket.air_speed / rocket.max_speed) / 100 + 1
        scale = cubic_bezier(0, 0, 50, 0, 100, rocket.max_speed / 20, 50, rocket.max_speed / 20, rocket.air_speed / rocket.max_speed) / 100 + 1

        # For debug info
        if not first and DEBUG == True:
            debug.info(screen, debug_font, rocket, last_speed, chunk_coordinates, scale, real_dt, highest_dt)
        else:
            first = False

        last_speed = rocket.speed

        # Read HID inputs ONLY FOR QUITTING THE GAME
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.save_data()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYUP:
                if keys[pygame.K_SPACE] or keys[pygame.K_ESCAPE]:
                    game_state = PAUSED

                elif keys[pygame.K_F1]:
                    DEBUG = not DEBUG
                    rocket.debug = DEBUG

                #Pressing the "R" key, resets the rocket
                elif keys[pygame.K_r]:
                    rocket.reset(player)
                    wind_timer = 0
                    wind_strength = 0

        # Update the screen
        pygame.display.update()

        time22 = get_time()

        # Apply running fps
        dt = timer.tick(fps) * 0.001

def upgrades():
    print(player.load_data())
    print(player.max_speed_level)

    UPGRADES_TEXT = get_font(45).render("UPGRADES", True, TEXT_HEADER_COLOR)
    UPGRADES_RECT = UPGRADES_TEXT.get_rect(center=(WIDTH / 2, 50))

    flash_timer = 0
    flash_message = None

    bar_amount = 4
    start_y, stop_y = 200, HEIGHT - 300
    y_position = range(start_y, stop_y, int((stop_y - start_y) / (bar_amount - 1)))

    MAGNET_STRENGTH_TEXT = get_font(15).render("Magnet strength:", True, TEXT_DEFAULT_COLOR)
    MAGNET_STRENGTH_RECT = MAGNET_STRENGTH_TEXT.get_rect(midright=(WIDTH / 2 - UPGRADES_BAR_WIDTH / 2, y_position[0]))
    MAGNET_STRENGTH_BAR = ProgressBarWithSteps((WIDTH / 2, y_position[0]), 
                                                   left_arrow_default, left_arrow_hover, 
                                                   right_arrow_default, right_arrow_hover,
                                                   BAR_COLOR, player.magnet_level, 0, 4, UPGRADES_BAR_WIDTH, "magnet_level")
    
    ROCKET_SPEED_TEXT = get_font(15).render("Rocket speed:", True, TEXT_DEFAULT_COLOR)
    ROCKET_SPEED_RECT = ROCKET_SPEED_TEXT.get_rect(midright=(WIDTH / 2 - UPGRADES_BAR_WIDTH / 2, y_position[1]))
    ROCKET_SPEED_BAR = ProgressBarWithSteps((WIDTH / 2,y_position[1]), 
                                                left_arrow_default, left_arrow_hover, 
                                                right_arrow_default, right_arrow_hover,
                                                BAR_COLOR, player.max_speed_level, 0, 5,  UPGRADES_BAR_WIDTH, "max_speed_level")
    

    ROCKET_FUEL_TEXT = get_font(15).render("Rocket fuel:", True, TEXT_DEFAULT_COLOR)
    ROCKET_FUEL_RECT = ROCKET_FUEL_TEXT.get_rect(midright=(WIDTH / 2 - UPGRADES_BAR_WIDTH / 2, y_position[2]))
    ROCKET_FUEL_BAR = ProgressBarWithSteps((WIDTH / 2, y_position[2]), 
                                                left_arrow_default, left_arrow_hover, 
                                                right_arrow_default, right_arrow_hover,
                                                BAR_COLOR, player.fuel_level, 0, 5, UPGRADES_BAR_WIDTH, "fuel_level")
    
    MAP_SIZE_TEXT = get_font(15).render("Map size:", True, TEXT_DEFAULT_COLOR)
    MAP_SIZE_RECT = MAP_SIZE_TEXT.get_rect(midright=(WIDTH / 2 - UPGRADES_BAR_WIDTH / 2, y_position[3]))
    MAP_SIZE_BAR = ProgressBarWithSteps((WIDTH / 2, y_position[3]), 
                                                left_arrow_default, left_arrow_hover, 
                                                right_arrow_default, right_arrow_hover,
                                                BAR_COLOR, player.map_level, 0, 7, UPGRADES_BAR_WIDTH, "map_level")

    BACK = Button((WIDTH/2, HEIGHT - 75), "BACK", get_font(75), TEXT_DEFAULT_COLOR, TEXT_HOVER_COLOR)

    run = True

    UPGRADE_COSTS = {
        "magnet_level": [10,20,30,40],
        "max_speed_level": [15,30,45,60,75],
        "fuel_level": [12, 24, 36, 48, 60],
        "map_level": [5, 10, 15, 20, 25, 30, 35]
    }

    def upgrade_stat(stat_name, current_level):
        if current_level < len(UPGRADE_COSTS[stat_name]):
            cost = UPGRADE_COSTS[stat_name][current_level]
            if player.money >= cost:
                player.money -= cost
                setattr(player, stat_name, current_level + 1)
                print(f"{stat_name} upgraded to level {current_level + 1}")
                flash_message = get_font(30).render(f"{stat_name} upgraded to level {current_level + 1}", True, (255, 255, 255))
            else:
                print("Not enough money to upgrade")
                flash_message = get_font(30).render("Not enough money to upgrade", True, (255, 0, 0))
        else:
            print(f"{stat_name} is already at maximum level")
            flash_message = get_font(30).render(f"{stat_name} is already at maximum level", True, (255, 255, 255))
        return flash_message

    def update_bars():
        MAGNET_STRENGTH_BAR.level = player.magnet_level
        ROCKET_SPEED_BAR.level = player.max_speed_level
        ROCKET_FUEL_BAR.level = player.fuel_level
        MAP_SIZE_BAR.level = player.map_level

    while run:

        keys = pygame.key.get_pressed()
        MOUSE_POS = pygame.mouse.get_pos()

        screen.fill(UPGRADES_BACKGROUND_COLOR)
        screen.blit(UPGRADES_TEXT, UPGRADES_RECT)

        BACK.changeColor(MOUSE_POS)
        BACK.update(screen)

        press = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.save_data()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                press = True
                if BACK.checkForInput(MOUSE_POS):
                    player.save_data()
                    run = False
        if keys[pygame.K_ESCAPE]:
            player.save_data()
            run = False

        if flash_message and flash_timer < 60:
            screen.blit(flash_message, (WIDTH / 2 - flash_message.get_width() / 2, HEIGHT / 2))
            flash_timer += 1
        elif flash_timer >= 60:
            flash_message = None
            flash_timer = 0

        screen.blit(MAGNET_STRENGTH_TEXT, MAGNET_STRENGTH_RECT)
        screen.blit(ROCKET_SPEED_TEXT, ROCKET_SPEED_RECT)
        screen.blit(ROCKET_FUEL_TEXT, ROCKET_FUEL_RECT)
        screen.blit(MAP_SIZE_TEXT, MAP_SIZE_RECT)

        magnet_level = MAGNET_STRENGTH_BAR.update(screen, MOUSE_POS, player, UPGRADE_COSTS, press)
        if player.magnet_level != magnet_level:
            flash_message = upgrade_stat("magnet_level", magnet_level)

        max_speed_level = ROCKET_SPEED_BAR.update(screen, MOUSE_POS, player, UPGRADE_COSTS, press)
        if player.max_speed_level != max_speed_level:
            flash_message = upgrade_stat("max_speed_level", max_speed_level)

        fuel_level = ROCKET_FUEL_BAR.update(screen, MOUSE_POS, player, UPGRADE_COSTS, press)
        if player.fuel_level != fuel_level:
            flash_message = upgrade_stat("fuel_level", fuel_level)

        map_level = MAP_SIZE_BAR.update(screen, MOUSE_POS, player, UPGRADE_COSTS, press)
        if player.map_level != map_level:
            flash_message = upgrade_stat("map_level", map_level)

        if (player.magnet_level != magnet_level or player.max_speed_level != max_speed_level or
            player.fuel_level != fuel_level or player.map_level != map_level):
            player.magnet_level = magnet_level
            player.max_speed_level = max_speed_level
            player.fuel_level = fuel_level
            player.map_level = map_level

        pygame.display.update()
        timer.tick(60)

def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("ROCKETMAN", True, TEXT_HEADER_COLOR)
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2, 100))

        # All avaliable buttons on the screen
        PLAY_BUTTON = Button((WIDTH / 2, 250), "PLAY", get_font(70), TEXT_DEFAULT_COLOR, TEXT_HOVER_COLOR, bg_color=TEXT_BACKGROUND_COLOR)
        UPGRADES_BUTTON = Button((WIDTH / 2, 400), "UPGRADES", get_font(70), TEXT_DEFAULT_COLOR, TEXT_HOVER_COLOR, bg_color=TEXT_BACKGROUND_COLOR)
        QUIT_BUTTON = Button((WIDTH / 2, 550), "QUIT", get_font(70), TEXT_DEFAULT_COLOR, TEXT_HOVER_COLOR, bg_color=TEXT_BACKGROUND_COLOR)

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
        timer.tick(60)

main_menu()

    
#pygame.quit()
            
    
        
