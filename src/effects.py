import random
from math import *
from coordinate_systems import world_to_screen_coordinates

from bezier_and_map import *


class Wind:
    def __init__(self, max_strength: int, time_range: list[float, float], wind_chance: int, left_image, right_image):
        self.max_strength = max_strength

        self.min_time = time_range[0]
        self.max_time = time_range[1]

        self.wind_chance = wind_chance

        self.left_image = left_image
        self.right_image = right_image
        
        self.timer = 0
        self.direction = 0
        self.strength = 0

    def create_chance_of_wind(self):
        if self.timer == 0:
            self.timer = (random.randint(0, self.wind_chance) == 1) * map_value(random.random(), 0, 1, self.min_time, self.max_time)
            self.strength = random.randint(1, self.max_strength)
            self.direction = [-1, 1][random.randint(0, 1)]

    def update(self, rocket, dt):
        if self.timer != 0:
            self.timer -= dt
            if self.timer <= 0:
                self.timer = 0
            rocket.angle += sin(radians(rocket.angle + 90)) * dt * self.direction * self.strength
            rocket.speed = (rocket.speed[0] + self.direction * self.strength * dt * 10, rocket.speed[1])

    def draw(self, screen, rocket, scale):
        if self.strength > 0 and self.timer != 0:
            if self.direction < 0:
                wind_scaled_image = pygame.transform.scale_by(self.right_image, scale)
                arrow_position = world_to_screen_coordinates(rocket.position, rocket.screen_center, scale)
                arrow_position = (arrow_position[0] + 100 * scale - wind_scaled_image.get_width() / 2, arrow_position[1] - wind_scaled_image.get_height() / 2)
                screen.blit(wind_scaled_image, arrow_position)
            elif self.direction > 0:
                wind_scaled_image = pygame.transform.scale_by(self.left_image, scale)
                arrow_position = world_to_screen_coordinates(rocket.position, rocket.screen_center, scale)
                arrow_position = (arrow_position[0] - 100 * scale - wind_scaled_image.get_width() / 2, arrow_position[1] - wind_scaled_image.get_height() / 2)
                screen.blit(wind_scaled_image, arrow_position)
