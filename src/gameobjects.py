from CONSTANTS import *
from math import *
from bezier import *
from coordinate_systems import *
import pygame

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

    def update(self, angle: float, screen_x_offset: int, screen_y_offset: int, scale: float) -> tuple[float, float]:
        angle = radians(angle) + atan2(self.y_offset, self.x_offset)
        self.x_pos = screen_x_offset + self.radius * cos(angle) * scale
        self.y_pos = screen_y_offset - self.radius * sin(angle) * scale
        return self.screen_position

    def draw(self, screen, scale, img_size, img_offset, color, angle):
        
        pygame.draw.circle(screen, color, self.update(angle, img_offset[0], img_offset[1], scale), 1)

class Rocket:
    def __init__(self, x_pos, y_pos, acceleration, boost, max_speed, collision_points, rocket_image_og):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.acceleration = acceleration
        self.boost = boost
        self.max_speed = max_speed
        self.angle = 0
        self.x_speed = 0
        self.y_speed = 0
        self.collision_points = []
        self.rocket_image_og = rocket_image_og
        for point in collision_points:
            self.collision_points.append(CollisionPoint(point))

    def draw(self, screen, scale: float, img_size: tuple[int, int]):
        # Put the image in the center of our imaginary "position point" aka when rotating the rocket
        # it rotates from the center, not from the upper left corner of the image (sprite)
        # Also apply scale to the rocket

        x_img_offset = cubic_bezier(0, 0, 50, 0, 50, 100, 100, 100, self.x_speed / self.max_speed) #,screen, position=(WIDTH - 100, HEIGHT - 100))
        y_img_offset = cubic_bezier(0, 0, 50, 0, 50, 100, 100, 100, self.y_speed / self.max_speed) #,screen, color='blue',position=(WIDTH - 100, HEIGHT- 200))
        img_x = WIDTH / 2 - x_img_offset * WIDTH / (2 * 100)
        img_y = HEIGHT / 2 + y_img_offset * HEIGHT / (2 * 100)

        rocket_image_scaled = pygame.transform.scale(self.rocket_image_og, (img_size[0] * scale, img_size[1] * scale))
        rocket_image_scaled_and_rotated = pygame.transform.rotate(rocket_image_scaled, self.angle)
        rocket_image_rect = rocket_image_scaled_and_rotated.get_rect(center = (img_x, img_y))
        screen.blit(rocket_image_scaled_and_rotated, rocket_image_rect)

        return (img_x, img_y)

    def update(self, screen, dt, scale, keys):
        """ Update the rockets position."""

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
        #Pressing the "R" key, resets everything
        if keys[pygame.K_r]:
            self.x_pos = WIDTH / 2
            self.y_pos = HEIGHT / 2
            self.x_speed = 0
            self.y_speed = 0
            self.angle = 0

        # Limit the speeds to be in range of maximum speed
        air_speed = sqrt(self.x_speed ** 2 + self.y_speed ** 2)
        if air_speed > self.max_speed:
            self.x_speed = self.max_speed / air_speed * self.x_speed
            self.y_speed = self.max_speed / air_speed * self.y_speed
        
        self.x_pos -= self.x_speed * dt
        self.y_pos += self.y_speed * dt

        # print(x_offset_amount, y_offset_amount)

        img_size = self.rocket_image_og.get_width(), self.rocket_image_og.get_height()

        lowest = None
        for index, point in enumerate(self.collision_points):
            point_y_position = point.screen_position[1]
            if lowest is None or lowest.screen_position[1] < point_y_position:
                lowest = point

        # If the lowest point intersects with ground
        if screen_to_world_coordinates((None, lowest.screen_position[1]), self.position, scale)[1] > HEIGHT / 2 + C_HEIGHT / 2:
            pygame.draw.circle(screen, "green", lowest.screen_position, 3)
            self.y_pos += (world_to_screen_coordinates((None, HEIGHT / 2 + C_HEIGHT / 2 + 2), self.position, scale)[1] - lowest.screen_position[1])
            self.x_speed = self.x_speed - self.x_speed * GROUND_FRICTION
            self.y_speed = 0 

        img_offset = self.draw(screen, scale, img_size)

        for index, point in enumerate(self.collision_points):
            point.draw(screen, scale, img_size, img_offset, COLORS[index % 8], self.angle)

        return air_speed
    
    @property
    def position(self):
        return (self.x_pos, self.y_pos)

class PowerUp:
    def __init__(self, type: str, level: int, position: tuple[int, int], visual):
        self.type = type # fuel, money
        self.level = level # 1,2,3
        self.position = position # world position
        self.visual = visual
    
    def draw(self, screen, scale, rocket_position):
        img_size = self.visual.get_width(), self.visual.get_height()
        scaled_visual = pygame.transform.scale(self.visual, (img_size[0] * scale * 3, img_size[1] * scale * 3))
        screen_position = world_to_screen_coordinates(self.position, rocket_position, scale)
        if screen_position[0] >= -100 and screen_position[0] <= WIDTH + 100 and screen_position[1] >= -100 and screen_position[1] <= HEIGHT + 100:
            power_up_rect = scaled_visual.get_rect(center = screen_position)
            screen.blit(scaled_visual, power_up_rect)
