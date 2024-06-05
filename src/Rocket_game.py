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
from effects import *

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

plane_img = pygame.image.load(PATH + "/images/missing_texture.png").convert_alpha()
helicopter_img = pygame.image.load(PATH + "/images/missing_texture.png").convert_alpha()
hot_air_balloon_img = pygame.image.load(PATH + "/images/missing_texture.png").convert_alpha()
cloud_img = pygame.image.load(PATH + "/images/missing_texture.png").convert_alpha()
fighter_jet_img = pygame.image.load(PATH + "/images/missing_texture.png").convert_alpha()
UFO_img = pygame.image.load(PATH + "/images/missing_texture.png").convert_alpha()
satellite_img = pygame.image.load(PATH + "/images/missing_texture.png").convert_alpha()



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
          "plane": plane_img, "helicopter": helicopter_img, "hot_air_balloon": hot_air_balloon_img, "cloud": cloud_img, #level 1
          "fighter_jet": fighter_jet_img,   # level 2
          "UFO": UFO_img, "satellite": satellite_img, #level 3
          None: missing_texture} 

def input():
    """ Keyboard input handling."""
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

# HAS TO ALWAYS BE HERE, SO THAT ALL FUNCTION (PLAY, UPGRADE, ...) CAN REACH IT
player = Player(DEFAULT_PLAYER_DATA) # all of it in player.py


def get_time():
    return time.perf_counter_ns()

def get_font(size):
    return pygame.font.Font(PATH + "/images/font.ttf", size)

def load_error(load_state):
    screen_time = 9
    error_text = get_font(20).render(str(load_state), True, 'red', 'black')
    error_text_rect = error_text.get_rect(center = (WIDTH / 2, HEIGHT / 2 - 30))

    recommendation = get_font(20).render("Save data is corrupted or not present.", True, 'red', 'black')
    recommendation_rect = recommendation.get_rect(center = (WIDTH / 2, HEIGHT / 2))

    progress = get_font(27).render("Progress will reset, if you continue", True, 'red', 'black')
    progress_rect = progress.get_rect(center = (WIDTH / 2, HEIGHT / 2 + 30))
    while True:
        screen.fill('black')
        screen.blit(error_text, error_text_rect)
        screen.blit(recommendation, recommendation_rect)
        screen.blit(progress, progress_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                screen_time = -1
        
        screen_time -= timer.tick(15) * 0.001
        if screen_time <= 0:
            break

def draw_ui(rocket, wind, money, scale):
    
    money.draw(screen, str(player.money))

    money_and_fuel = debug_font.render(f"Money: {player.money} | Fuel: {round(rocket.fuel,0)}", True, 'black', 'white')
    screen.blit(money_and_fuel, (WIDTH // 2 - money_and_fuel.get_width() // 2, 0))
    if rocket.disabled > 0:
        if (rocket.disabled - int(rocket.disabled) < 0.5):
                screen.blit(danger, (WIDTH / 2 - danger.get_width() / 2, HEIGHT / 2 - danger.get_height() / 2))

    wind.draw(screen, rocket, scale)
    

def play():
    # FOR PAUSE MENU (BUTTONS AND STUFF)
    MENU_TEXT = get_font(100).render("PAUSED", True, TEXT_HEADER_COLOR)
    MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2, 100))

    # All avaliable buttons on the screen
    CONTINUE_BUTTON = Button((WIDTH / 2, 250), "CONTINUE", get_font(70), TEXT_DEFAULT_COLOR, TEXT_HOVER_COLOR, bg_color = TEXT_BACKGROUND_COLOR)
    RESTART_BUTTON = Button((WIDTH / 2, 400), "RESTART", get_font(70), TEXT_DEFAULT_COLOR, TEXT_HOVER_COLOR, bg_color = TEXT_BACKGROUND_COLOR)
    MAIN_MENU_BUTTON = Button((WIDTH / 2, 550), "MAIN MENU", get_font(70), TEXT_DEFAULT_COLOR, TEXT_HOVER_COLOR, bg_color = TEXT_BACKGROUND_COLOR)


    # LOAD GAME DATA
    load_state = player.load_data()
    if 1 not in load_state.keys():
        load_error(load_state)
            
    # INITialize the objects
    #collision_points = [[1,49],[25,-1],[13,-50],[-11,-50], [-23,-1]]
    collision_points = [[0, 87], [22, 47], [47, -35], [22, -52], [-22, -52], [-47, -35], [-22, 47]]

    max_speed = player.starting_speed + player.max_speed_level * ROCKET_SPEED_MULTIPLIER
    start_fuel = player.starting_fuel + player.fuel_level * FUEL_LEVEL_MULTIPLIER
    #                 start_x,  start_y,     acceleration,
    #                    |         |         |   boost acceleration,
    #                    |         |         |   |   maximum speed
    #                    |         |         |   |   |          start_fuel
    #                    |         |         |   |   |          |           points for collision
    #                    |         |         |   |   |          |           |                image
    #                    |         |         |   |   |          |           |                |
    rocket = Rocket((WIDTH / 2, 511), 4, 8, max_speed, start_fuel, collision_points, rocket_image) # Rocket in gameobjects.py

    


    background = Background(2 * CHUNK_GEN_RADIUS + 1, debug_font) # Background in background.py

    minimap = MiniMap(player.map_level) # Minimap in gameobjects.py

    clouds = pygame.sprite.Group()
    clouds.add(Cloud((random.randint(0, WIDTH),random.randint(0, HEIGHT)), cloud_image_0, 1.2))
    clouds.add(Cloud((random.randint(0, WIDTH),random.randint(0, HEIGHT)), cloud_image_1, 1.15))
    clouds.add(Cloud((random.randint(0, WIDTH),random.randint(0, HEIGHT)), cloud_image_2, 1.1))

    clouds.add(Cloud((random.randint(0, WIDTH),random.randint(0, HEIGHT)), cloud_image_3, 1.05))
    clouds.add(Cloud((random.randint(0, WIDTH),random.randint(0, HEIGHT)), cloud_image_4, 1.03))
    clouds.add(Cloud((random.randint(0, WIDTH),random.randint(0, HEIGHT)), cloud_image_5, 1.01))

    wind = Wind(MAX_WIND_STRENGTH, WIND_DURATION, WIND_CHANCE, wind_left, wind_right)

    DEBUG = True
    scale = 1
    run = True
    first = True
    frame_time = 0
    dt = 0.016
    collision_group = pygame.sprite.Group()
    
    game_state = PLAYING
    chunk_coordinates = (0,-1)
    last_speed = (0,0)

    rocket.reset(player)
    money = Price((20, HEIGHT - 20), coin_img, get_font(15), 'white')

    while run:
        """ if game_state == PAUSED:
            game_state, run = pause_menu(rocket, background, minimap, chunk_coordinates, collision_group, clouds, wind_strength, money, scale)
            continue """

        # For FPS counter
        dt = (time.perf_counter_ns() - frame_time) / 1_000_000_000 # Because it is in nanoseconds
        frame_time = time.perf_counter_ns()

        if first:
            create_objects_for_the_first_time(collision_group, images)
            screen.fill(SKY_COLOR)
            dt = 0.016
            first = False

        # Fill the screen with background color
        screen.fill(gradient(chunk_coordinates[1] + 2))

        # Get input from keyboard mouse (HID)
        keys = input()

        # Check for collisions, if player died, reset the wind
        check_collisions(player, rocket, collision_group, images)

        # Draw parallaxed clouds
        for cloud in clouds:
            cloud.draw(screen, rocket.screen_center, scale)

        # Update and draw background (right now the ground)
        chunk_coordinates = background.update(screen, scale, rocket.screen_center, ground, DEBUG)

        if game_state == PLAYING:
            # Calculate new rocket position and draw the rocket
            rocket.update(screen, dt, scale, keys, player)
            wind.create_chance_of_wind()
            wind.update(rocket, dt)
        rocket.draw(screen, scale)

        # Load and unload objects if they are too far from the rocket.
        objects_load_unload(collision_group, chunk_coordinates, images)

        # Draw the minimap base
        if player.map_level > 0:
            minimap.draw_base(screen, rocket.position)

        # Go through all objects and move as well as draw them on the screen and on the minimap
        for object in collision_group:
            if object.type in MAGNETIC_OBJECTS:
                object.move_towards(rocket.position, rocket.speed, player, dt)
            if game_state ==  PLAYING:
                object.update()
            object.draw(screen, rocket.screen_center, scale)
            
            # Draw all objects (fuel, money, obstacles) onto the minimap
            if player.map_level > 0:
                minimap.draw(screen, rocket.position, object, DEBUG)


        if game_state == PAUSED:
            draw_rect_alpha(screen, (0,0,0,50), pygame.Rect(0,0,WIDTH, HEIGHT))

            MOUSE_POS = pygame.mouse.get_pos()


            screen.blit(MENU_TEXT, MENU_RECT)

            for button in [CONTINUE_BUTTON, RESTART_BUTTON, MAIN_MENU_BUTTON]:
                button.changeColor(MOUSE_POS)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if keys[pygame.K_ESCAPE]:
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
                        game_state = PLAYING
                        break
                    if MAIN_MENU_BUTTON.checkForInput(MOUSE_POS):
                        player.save_data()
                        run = False
                        break

        # HERE GO ALL UI ELEMENTS
        draw_ui(rocket, wind, money, scale)
        

        # Calculate the scale 
        scale = cubic_bezier(0, 0, 50, 0, 100, rocket.max_speed / 20, 50, rocket.max_speed / 20, rocket.air_speed / rocket.max_speed) / 100 + 1

        # For debug info
        if not first and DEBUG == True:
            debug.info(screen, debug_font, rocket, last_speed, chunk_coordinates, scale, dt)

        last_speed = rocket.speed

        # Read HID inputs ONLY FOR QUITTING THE GAME
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.save_data()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYUP:
                if keys[pygame.K_SPACE] or keys[pygame.K_ESCAPE]:
                    if game_state == PLAYING:
                        game_state = PAUSED
                    elif game_state == PAUSED:
                        game_state = PLAYING

                elif keys[pygame.K_F1]:
                    DEBUG = not DEBUG
                    rocket.debug = DEBUG

                #Pressing the "R" key, resets the rocket
                elif keys[pygame.K_r] and DEBUG:
                    rocket.reset(player)

        # Update the screen
        pygame.display.update()

        # Apply running fps
        timer.tick(fps)

def upgrades():
    load_state = player.load_data()
    if 1 not in load_state.keys():
        load_error(load_state)

    UPGRADES_TEXT = get_font(45).render("UPGRADES", True, TEXT_HEADER_COLOR)
    UPGRADES_RECT = UPGRADES_TEXT.get_rect(center=(WIDTH / 2, 50))


    bar_amount = 4
    start_y, stop_y = 200, HEIGHT - 300
    y_position = range(start_y, stop_y, int((stop_y - start_y) / (bar_amount - 1)))
    text_size = 20
    bar_x_center = WIDTH / 1.6

    MAGNET_STRENGTH_TEXT = get_font(text_size).render("Magnet strength:", True, TEXT_DEFAULT_COLOR)
    MAGNET_STRENGTH_RECT = MAGNET_STRENGTH_TEXT.get_rect(midright=(bar_x_center - UPGRADES_BAR_WIDTH / 2, y_position[0]))
    MAGNET_STRENGTH_BAR = ProgressBarWithSteps((bar_x_center, y_position[0]), 
                                                   left_arrow_default, left_arrow_hover, 
                                                   right_arrow_default, right_arrow_hover,
                                                   BAR_COLOR, player.magnet_level, 0, len(UPGRADE_COSTS["magnet_level"]), UPGRADES_BAR_WIDTH)
    
    MAGNET_PRICE = Price((bar_x_center + UPGRADES_BAR_WIDTH / 2 + 10,y_position[0]), coin_img, get_font(text_size), 'white', 'gray', 'red', text_size)
                 
    
    ROCKET_SPEED_TEXT = get_font(text_size).render("Rocket speed:", True, TEXT_DEFAULT_COLOR)
    ROCKET_SPEED_RECT = ROCKET_SPEED_TEXT.get_rect(midright=(bar_x_center - UPGRADES_BAR_WIDTH / 2, y_position[1]))
    ROCKET_SPEED_BAR = ProgressBarWithSteps((bar_x_center,y_position[1]), 
                                                left_arrow_default, left_arrow_hover, 
                                                right_arrow_default, right_arrow_hover,
                                                BAR_COLOR, player.max_speed_level, 0, len(UPGRADE_COSTS["max_speed_level"]),  UPGRADES_BAR_WIDTH)

    ROCKET_SPEED_PRICE = Price((bar_x_center + UPGRADES_BAR_WIDTH / 2 + 10, y_position[1]), coin_img, get_font(text_size), 'white', 'gray', 'red', text_size)
    

    ROCKET_FUEL_TEXT = get_font(text_size).render("Rocket fuel:", True, TEXT_DEFAULT_COLOR)
    ROCKET_FUEL_RECT = ROCKET_FUEL_TEXT.get_rect(midright=(bar_x_center - UPGRADES_BAR_WIDTH / 2, y_position[2]))
    ROCKET_FUEL_BAR = ProgressBarWithSteps((bar_x_center, y_position[2]), 
                                                left_arrow_default, left_arrow_hover, 
                                                right_arrow_default, right_arrow_hover,
                                                BAR_COLOR, player.fuel_level, 0, len(UPGRADE_COSTS["fuel_level"]), UPGRADES_BAR_WIDTH)
    
    ROCKET_FUEL_PRICE = Price((bar_x_center + UPGRADES_BAR_WIDTH / 2 + 10, y_position[2]), coin_img, get_font(text_size), 'white', 'gray', 'red', text_size)
    
    MAP_SIZE_TEXT = get_font(text_size).render("Map size:", True, TEXT_DEFAULT_COLOR)
    MAP_SIZE_RECT = MAP_SIZE_TEXT.get_rect(midright=(bar_x_center - UPGRADES_BAR_WIDTH / 2, y_position[3]))
    MAP_SIZE_BAR = ProgressBarWithSteps((bar_x_center, y_position[3]), 
                                                left_arrow_default, left_arrow_hover, 
                                                right_arrow_default, right_arrow_hover,
                                                BAR_COLOR, player.map_level, 0, len(UPGRADE_COSTS["map_level"]), UPGRADES_BAR_WIDTH)
    MAP_SIZE_PRICE = Price((bar_x_center + UPGRADES_BAR_WIDTH / 2 + 10, y_position[3]), coin_img, get_font(text_size), 'white', 'gray', 'red', text_size)

    BACK = Button((WIDTH/2, HEIGHT - 75), "BACK", get_font(75), TEXT_DEFAULT_COLOR, TEXT_HOVER_COLOR)

    run = True

    current_money = Price((20, 20), coin_img, get_font(text_size), 'white', height=text_size)
    while run:
        keys = input()
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


        current_money.draw(screen, str(player.money))

        # MAGNET LEVEL
        screen.blit(MAGNET_STRENGTH_TEXT, MAGNET_STRENGTH_RECT)
        level_change = MAGNET_STRENGTH_BAR.update(screen, MOUSE_POS, press)

        state = "default"

        
        if level_change == 1 and player.money >= UPGRADE_COSTS["magnet_level"][player.magnet_level + level_change - 1]:
            player.magnet_level += level_change
            player.money -= UPGRADE_COSTS["magnet_level"][player.magnet_level - 1]

        elif level_change == -1 and player.magnet_level > 0:
            player.money += UPGRADE_COSTS["magnet_level"][player.magnet_level - 1]
            player.magnet_level += level_change 
        elif player.magnet_level < len(UPGRADE_COSTS["magnet_level"]) and player.money < UPGRADE_COSTS["magnet_level"][player.magnet_level]:
            state = "insufficient"

        if player.magnet_level == MAGNET_STRENGTH_BAR.max_value:
            price = "MAX"
            state = "disabled"
        else:
            price = UPGRADE_COSTS["magnet_level"][player.magnet_level]

        MAGNET_STRENGTH_BAR.draw(screen, player.magnet_level)
        MAGNET_PRICE.draw(screen, str(price), state)
        


        # ROCKET SPEED
        screen.blit(ROCKET_SPEED_TEXT, ROCKET_SPEED_RECT)
        level_change = ROCKET_SPEED_BAR.update(screen, MOUSE_POS, press)

        state = "default"
        if level_change == 1 and player.money >= UPGRADE_COSTS["max_speed_level"][player.max_speed_level + level_change - 1]:
            player.max_speed_level += level_change
            player.money -= UPGRADE_COSTS["max_speed_level"][player.max_speed_level - 1]
        elif level_change == -1 and player.max_speed_level > 0:
            player.money += UPGRADE_COSTS["max_speed_level"][player.max_speed_level - 1]
            player.max_speed_level += level_change 
        elif player.max_speed_level < len(UPGRADE_COSTS["max_speed_level"]) and player.money < UPGRADE_COSTS["max_speed_level"][player.max_speed_level]:
            state = "insufficient"

        if player.max_speed_level == ROCKET_SPEED_BAR.max_value:
            price = "MAX"
            state = "disabled"
        else:
            price = UPGRADE_COSTS["max_speed_level"][player.max_speed_level]

        ROCKET_SPEED_BAR.draw(screen, player.max_speed_level)
        ROCKET_SPEED_PRICE.draw(screen, str(price), state)
        
        # ROCKET FUEL
        screen.blit(ROCKET_FUEL_TEXT, ROCKET_FUEL_RECT)
        level_change = ROCKET_FUEL_BAR.update(screen, MOUSE_POS, press)

        state = "default"
        if level_change == 1 and player.money >= UPGRADE_COSTS["fuel_level"][player.fuel_level + level_change - 1]:
            player.fuel_level += level_change
            player.money -= UPGRADE_COSTS["fuel_level"][player.fuel_level - 1]
        elif level_change == -1 and player.fuel_level > 0:
            player.money += UPGRADE_COSTS["fuel_level"][player.fuel_level - 1]
            player.fuel_level += level_change 
        elif player.fuel_level < len(UPGRADE_COSTS["fuel_level"]) and  player.money < UPGRADE_COSTS["fuel_level"][player.fuel_level]:
            state = "insufficient"

        if player.fuel_level == ROCKET_FUEL_BAR.max_value:
            price = "MAX"
            state = "disabled"
        else:
            price = UPGRADE_COSTS["fuel_level"][player.fuel_level]

        ROCKET_FUEL_BAR.draw(screen, player.fuel_level)
        ROCKET_FUEL_PRICE.draw(screen, str(price), state)

        
        # MAP LEVEL
        screen.blit(MAP_SIZE_TEXT, MAP_SIZE_RECT)
        level_change = MAP_SIZE_BAR.update(screen, MOUSE_POS, press)

        state = "default"
        if level_change == 1 and player.money >= UPGRADE_COSTS["map_level"][player.map_level + level_change - 1]:
            player.map_level += level_change
            player.money -= UPGRADE_COSTS["map_level"][player.map_level - 1]
        elif level_change == -1 and player.map_level > 0:
            player.money += UPGRADE_COSTS["map_level"][player.map_level - 1]
            player.map_level += level_change 
        elif player.map_level < len(UPGRADE_COSTS["map_level"]) and player.money < UPGRADE_COSTS["map_level"][player.map_level]:
            state = "insufficient"
            

        if player.map_level == MAP_SIZE_BAR.max_value:
            price = "MAX"
            state = "disabled"
        else:
            price = UPGRADE_COSTS["map_level"][player.map_level]

        MAP_SIZE_BAR.draw(screen, player.map_level)
        MAP_SIZE_PRICE.draw(screen, str(price), state)

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