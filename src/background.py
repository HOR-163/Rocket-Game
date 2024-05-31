from CONSTANTS import *
import pygame
from bezier_and_map import map_value
from coordinate_systems import *
from math import *

def gradient(y: int):
    color1 = (176, 230, 235)
    color2 = (0,0,255)
    color3 = (0,0,0)
    stop1 = 0
    stop2 = 150
    stop3 = 300

    result = color3

    if stop1 <= y < stop2:
        percent = map_value(y, stop1, stop2, 0, 1)
        result = (color1[0] + percent * (color2[0] - color1[0]),
                  color1[1] + percent * (color2[1] - color1[1]),
                  color1[2] + percent * (color2[2] - color1[2]))
    elif stop2 <= y < stop3:
        percent = map_value(y, stop2, stop3, 0, 1)
        result = (color2[0] + percent * (color3[0] - color2[0]),
                  color2[1] + percent * (color3[1] - color2[1]),
                  color2[2] + percent * (color3[2] - color2[2]))
    return result


class Cloud(pygame.sprite.Sprite):
    def __init__(self, position, image, parallax_multiplier):
        self.position = position
        self.image = image
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.parallax_multiplier = parallax_multiplier
        pygame.sprite.Sprite.__init__(self)
    

    def draw(self, screen, screen_center, scale):
        scale1 = scale / self.parallax_multiplier

        screen_position = world_to_screen_coordinates(self.position, screen_center, scale1)
        screen_position = (screen_position[0] / self.parallax_multiplier, screen_position[1] / self.parallax_multiplier)

        if screen_position[1] >= HEIGHT + self.image_height:
            screen_position = (random.randint(0, WIDTH), 0 - self.image_height)
            self.position = screen_to_world_coordinates(screen_position, screen_center, scale1)
        elif screen_position[1] <= 0 - self.image_height:
            screen_position = (random.randint(0, WIDTH), HEIGHT * self.parallax_multiplier + self.image_height)
            self.position = screen_to_world_coordinates(screen_position, screen_center, scale1)

        if screen_position[0] >= WIDTH + self.image_width:
            screen_position = (0 - self.image_width, random.randint(0, HEIGHT))
            self.position = screen_to_world_coordinates(screen_position, screen_center, scale1)
        elif screen_position[0] <= 0 - self.image_width:
            screen_position = (WIDTH * self.parallax_multiplier + self.image_width, random.randint(0, HEIGHT))
            self.position = screen_to_world_coordinates(screen_position, screen_center, scale1)

        if self.position[1] > C_HEIGHT:
            return

        #print(self.position)
        scaled_image = pygame.transform.scale(self.image, (self.image_width * scale, self.image_height * scale))

        #print(self.position)
        self.rect = scaled_image.get_rect(center = screen_position)
        screen.blit(scaled_image, self.rect)



class Background:
    """Handle background."""

    def __init__(self, load_radius: int, DEBUG_FONT):
        # how many chunks to load (e.g 3x3 amount of chunks)
        self.load_radius = load_radius

        self.DEBUG = True
        self.DEBUG_FONT = DEBUG_FONT

    def update(self, screen, scale, rocket_position: tuple[float, float],ground,  DEBUG= False):
        self.DEBUG = DEBUG

        chunk_x, chunk_y = world_to_chunk_coordinates(rocket_position)
        #top_left_chunk_world_coords = chunk_to_world_coordinates((chunk_x - self.load_radius, -chunk_y - self.load_radius))

        for y_offset in range(int(-self.load_radius / 2) + 1, int(self.load_radius / 2) + 2):
            #background = gradient(chunk_y + y_offset)
            for x_offset in range(int(-self.load_radius / 2), int(self.load_radius / 2) + 1):

                world_x, world_y = chunk_to_world_coordinates((chunk_x + x_offset, -chunk_y - y_offset))

                chunk_screen_coordinates = world_to_screen_coordinates((world_x, -world_y), rocket_position, scale)
                
                # Draw the ground
                if chunk_y + y_offset < 0 and chunk_screen_coordinates[0] >= -C_WIDTH and chunk_screen_coordinates[0] <= WIDTH and chunk_screen_coordinates[1] < HEIGHT:
                    scaled_ground = pygame.transform.scale(ground, (ground.get_width() * scale + 1, ground.get_height() * scale + 1))
                    screen.blit(scaled_ground, pygame.Rect(chunk_screen_coordinates[0], chunk_screen_coordinates[1], 
                                                                        ceil(C_WIDTH * scale) + 1, ceil(C_HEIGHT * scale) + 1)) 


                # Draw the rectangles
                """if chunk_y + y_offset >= 0:
                    pygame.draw.rect(screen, background, pygame.Rect(chunk_screen_coordinates[0], chunk_screen_coordinates[1], 
                                                                ceil(C_WIDTH * scale), ceil(C_HEIGHT * scale)))"""


                """ # Draw the ground
                if chunk_y + y_offset < 0:
                    pygame.draw.rect(screen, GROUND_COLOR, pygame.Rect(chunk_screen_coordinates[0], chunk_screen_coordinates[1], 
                                                                        ceil(C_WIDTH * scale), ceil(C_HEIGHT * scale))) """
                
                """if self.DEBUG:
                    # Create and find the size (length, height) of chunk text (mainly for debugging)
                    chunk_coordinates_str = f"{chunk_x + x_offset} {chunk_y + y_offset}"
                    chunk_coordinates_rendered = self.DEBUG_FONT.render(chunk_coordinates_str, True, 'black', 'white')
                    chunk_coordinates_str_size = self.DEBUG_FONT.size(chunk_coordinates_str)
                    chunk_coordinates_str_coordinates = (chunk_screen_coordinates[0] + C_WIDTH / 2 * scale - chunk_coordinates_str_size[0] / 2, 
                                                         chunk_screen_coordinates[1] + C_HEIGHT / 2 * scale - chunk_coordinates_str_size[1] / 2)
                    # Write the chunk coordinates to the screen (uses basically the same equations like in background drawing)
                    screen.blit(chunk_coordinates_rendered, chunk_coordinates_str_coordinates)

                    # Draw chunk borders
                    pygame.draw.rect(screen, 'red', pygame.Rect(chunk_screen_coordinates[0], chunk_screen_coordinates[1], 
                                            ceil(C_WIDTH * scale), ceil(C_HEIGHT * scale)), 1) """

        # For debugging
        return (chunk_x, chunk_y)