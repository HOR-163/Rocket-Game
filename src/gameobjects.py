import pygame
from math import *

from CONSTANTS import *
from bezier_and_map import *
from coordinate_systems import *
from extra_graphics import *


"""#################
   COLLISIONPOINT
#################"""

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

    def draw(self, screen, scale, image_size, image_offset, color, angle):
        
        pygame.draw.circle(screen, color, self.update(angle, image_offset[0], image_offset[1], scale), 1)

"""#########
   ROCKET
#########"""

class Rocket(pygame.sprite.Sprite):
    def __init__(self, position: tuple[float, float], acceleration, boost, max_speed, fuel, collision_points, image):

        # Rocket's position 
        self.position = position
        # The camera view's center
        self.screen_center = self.position

        # Acceleration
        self.acceleration = acceleration
        self.boost = boost

        # Speed and angle variables 
        self.max_speed = max_speed
        self.angle = 0
        self.speed = (0,0)
        self.air_speed = 0

        # fuel
        self.start_fuel = fuel
        self.fuel = fuel

        # Points for ground collision detection
        self.collision_points = []
        for point in collision_points:
            self.collision_points.append(CollisionPoint(point))

        # All variables for image transforming and collision detection
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image_size = self.image.get_width(), self.image.get_height()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.image_offset = (0,0)

        self.debug = True

        # If the rocket goes through a thunder cloud, a timer will count down until rocket's systems restore
        self.disabled = 0 # In seconds how long player can't control rocket

    def draw(self, screen, scale: float):
        # Put the image in the center of our imaginary "position point" aka when rotating the rocket
        # it rotates from the center, not from the upper left corner of the image (sprite)
        # Also apply scale to the rocket
        x_image_offset = cubic_bezier(0, 0, 50, 0, 50, self.max_speed / 20, 100, self.max_speed / 20, self.speed[0] / self.max_speed) #,screen, position=(WIDTH - 100, HEIGHT - 100))
        y_image_offset = cubic_bezier(0, 0, 50, 0, 50, self.max_speed / 20, 100, self.max_speed / 20, self.speed[1] / self.max_speed) #,screen, color='blue',position=(WIDTH - 100, HEIGHT- 200))


        image_x = WIDTH / 2 - x_image_offset * WIDTH / (2 * 100)
        image_y = HEIGHT / 2 + y_image_offset * HEIGHT / (2 * 100)

        self.image_offset = (image_x, image_y)
        

        scaled_image = pygame.transform.scale(self.image, (self.image_size[0] * scale, self.image_size[1] * scale))
        scaled_rotated_image = pygame.transform.rotate(scaled_image, self.angle)

        self.rect = scaled_rotated_image.get_rect(center = self.image_offset)
        self.mask = pygame.mask.from_surface(scaled_rotated_image)

        screen.blit(scaled_rotated_image, self.rect)


    def update(self, screen, dt, scale, keys, player):
        """ Update the rockets position."""
        if self.disabled > 0:
            self.disabled -= dt
        
        if self.disabled < 0:
            self.disabled = 0

        if self.fuel > 0:
            self.vertical_input(keys)
        
        else:
            self.fuel = 0
            self.speed = (self.speed[0] + cos(radians(self.angle - 90)), self.speed[1] + GRAVITY)
        
        self.rotational_input(keys, dt)

        # Limit the speeds to be in range of maximum speed
        self.air_speed = sqrt(self.speed[0] ** 2 + self.speed[1] ** 2)
        if self.air_speed > self.max_speed:
            self.speed = (self.max_speed / self.air_speed * self.speed[0],
                          self.max_speed / self.air_speed * self.speed[1])

        self.position = (self.position[0] - self.speed[0] * dt,
                         self.position[1] + self.speed[1] * dt)


        self.screen_center = screen_to_world_coordinates((WIDTH  - self.image_offset[0], HEIGHT  - self.image_offset[1]), self.position, scale)

        if self.position[1] > -C_HEIGHT:
            lowest = None
            for index, point in enumerate(self.collision_points):
                point_y_position = point.screen_position[1]
                if lowest is None or lowest.screen_position[1] < point_y_position:
                    lowest = point

            # If the lowest point intersects with ground
            if screen_to_world_coordinates((None, lowest.screen_position[1]), self.screen_center, scale)[1] > HEIGHT / 2 + C_HEIGHT / 2:
                if self.debug:
                    pygame.draw.circle(screen, "green", lowest.screen_position, 3)

                if self.speed[1] > 500 or self.fuel == 0:
                    self.reset(player)
                    return
                
                self.position = (self.position[0],
                                 self.position[1] + world_to_screen_coordinates((None, HEIGHT / 2 + C_HEIGHT / 2 + 1), self.position, scale)[1] - lowest.screen_position[1])
                self.speed = (self.speed[0] - self.speed[0] * GROUND_FRICTION, 0)

        for index, point in enumerate(self.collision_points):
            point.update(self.angle, self.image_offset[0], self.image_offset[1], scale)
            if self.debug:
                point.draw(screen, scale, self.image_size, self.image_offset, COLORS[index % 7], self.angle)
    
    def reset(self, player):
        self.position = (WIDTH / 2, HEIGHT / 2)
        self.speed = (0,0)
        self.angle = 0
        self.fuel = player.starting_fuel + player.fuel_level * FUEL_LEVEL_MULTIPLIER

    def vertical_input(self, keys):
        if self.disabled > 0:
            self.speed = (self.speed[0], self.speed[1] + GRAVITY)
            return
        # Pressing up so add boost
        if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.speed = (self.speed[0] + cos(radians(self.angle - 90)) * self.boost,
                              self.speed[1] + sin(radians(self.angle - 90)) * self.boost)
        # Pressing down, so no acceleration
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.speed[1] <= FALL_SPEED:
            self.speed = (self.speed[0], self.speed[1] + GRAVITY)
        # Pressing nothing, so we have to add acceleration
        else:
            self.speed = (self.speed[0] + cos(radians(self.angle - 90)) * self.acceleration,
                            self.speed[1] + sin(radians(self.angle - 90)) * self.acceleration)
            
        if not keys[pygame.K_s] and not keys[pygame.K_DOWN]:
            self.fuel -= self.air_speed / 30000
    
    def rotational_input(self, keys, dt):
        if self.disabled > 0:
            return
        # Pressing right, so rotate rocket clockwise
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle -= 20 * dt
        # Pressing left, so rotate rocket counter-clockwise
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle += 20 * dt



"""#######################################
   GAMEOBJECTS (MONEY, FUEL, OBSTACLES)
#######################################"""

class Object(pygame.sprite.Sprite):
    def __init__(self, type: str, level: int | None, position: tuple[int, int], image):
        self.type = type 
        self.level = level # 1,2,3
        self.position = position # world position
        self.chunk_coordinates = world_to_chunk_coordinates(self.position)

        # All variables for drawing the object and collision detection
        #pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.image = image
        
        self.mask = pygame.mask.from_surface(self.image)

        self.image_size = self.image.get_width(), self.image.get_height()
        self.rect = pygame.Rect(0,100000, self.image_size[0], self.image_size[1]) # move the rect to impossibly low, that the collsiion wouldn't occur on the first frame

        self.scale_overwrite = 1

        if self.type in MOVING_OBJECTS:
    
            if "horisontal" in MOVING_OBJECTS[self.type]:
                self.speed = (MOVING_OBJECTS[self.type]["horisontal"] * [-1,1][random.randint(0,1)],0)
            elif "vertical" in MOVING_OBJECTS[self.type]:
                self.speed = (0,MOVING_OBJECTS[self.type]["vertical"] * [-1,1][random.randint(0,1)])
            elif "all" in MOVING_OBJECTS[self.type]:
                self.speed = (MOVING_OBJECTS[self.type]["all"] * [-1,1][random.randint(0,1)],
                                     MOVING_OBJECTS[self.type]["all"] * [-1,1][random.randint(0,1)])
        else:
            self.speed = (0,0)

    def draw(self, screen, screen_center, scale):
        screen_position = world_to_screen_coordinates(self.position, screen_center, scale)
        if (screen_position[0] >= 0 - self.image_size[0] * 2 and 
            screen_position[0] <= WIDTH + self.image_size[0] * 2 and 
            screen_position[1] >= 0 - self.image_size[1] * 2 and 
            screen_position[1] <= HEIGHT + self.image_size[1] * 2 and 
            self.position[1] <= MINIMUM_OBJECT_HEIGHT):
            
            scaled_image = pygame.transform.scale(self.image, (self.image_size[0] * scale * self.scale_overwrite, self.image_size[1] * scale * self.scale_overwrite))
            self.mask = pygame.mask.from_surface(scaled_image)
            self.rect = scaled_image.get_rect(center = screen_position)
            screen.blit(scaled_image, self.rect)
    
    def move_towards(self, target_position, target_speed, player, dt):
        if self.position[1] <= MINIMUM_OBJECT_HEIGHT:
            move_vector = (target_position[0] - self.position[0], target_position[1] - self.position[1])
            vector_length = move_vector[0] ** 2 + move_vector[1] ** 2
            if vector_length <= (player.magnet_level * MAGNET_LEVEL_MULTIPLIER)  ** 2:
                self.speed = ((-target_speed[0] + (move_vector[0] / vector_length) * 30000) * dt, 
                                (target_speed[1] + (move_vector[1] / vector_length) * 30000) * dt)
    

    def update(self):
        if self.speed[0] != 0 and self.speed[1] != 0:
            self.position = (self.position[0] + self.speed[0], self.position[1] + self.speed[1])
            self.chunk_coordinates = world_to_chunk_coordinates(self.position)

        
        

class MiniMap:
    def __init__(self, visibility_radius):

        margin = (10,10)

        self.size = (WIDTH / 4, HEIGHT / 4)
        self.position = (WIDTH - self.size[0] - margin[0], 0 + margin[1])
        self.rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

        self.bg_color = (0,0,0,128)

        self.visibility_radius = visibility_radius

    def draw_base(self, screen, rocket_position):
        draw_rect_alpha(screen, self.bg_color, self.rect)

        # Draw the ground
        ground_position = self.world_to_map_coordinates((0, (HEIGHT + C_HEIGHT) // 2), rocket_position)
        if self.rect.top <= ground_position[1] <= self.rect.bottom:
            pygame.draw.rect(screen, GROUND_COLOR, pygame.Rect(self.rect.left, ground_position[1], self.size[0], self.rect.bottom - ground_position[1] + 1))

    def draw(self, screen, rocket_position, object, DEBUG=False):
        if object.type == "money":
            color = (0, 255, 0)
            object_level = object.level
        elif object.type == "fuel":
            color = (255, 255, 0)
            object_level = object.level
        elif object.type in ALL_OBSTACLES:
            color = (255, 0, 0)
            object_level = 3

        # Draw the objects
        if DEBUG:
            map_coordinates = self.world_to_map_coordinates(object.position, rocket_position)
            if (self.rect.left <= map_coordinates[0] <= self.rect.right and self.rect.top <= map_coordinates[1] <= self.rect.bottom):
                pygame.draw.circle(screen, color, map_coordinates, object_level)

        elif object.position[1] < -C_HEIGHT / 2 - C_HEIGHT:
            map_coordinates = self.world_to_map_coordinates(object.position, rocket_position)
            if (self.rect.left <= map_coordinates[0] <= self.rect.right and self.rect.top <= map_coordinates[1] <= self.rect.bottom):
                pygame.draw.circle(screen, color, map_coordinates, object_level)
            
            
            
            

        pygame.draw.circle(screen, 'white', (self.rect.left + self.rect.width / 2, self.rect.top + self.rect.height / 2), 2)
    
    def world_to_map_coordinates(self, world_coordinates: tuple[int, int], rocket_position):
        map_x, map_y = 0, 0
        normalised_coordinates = (world_coordinates[0] - rocket_position[0] + (self.visibility_radius + 0.5) * C_WIDTH, world_coordinates[1] - rocket_position[1] + (self.visibility_radius + 0.5) * C_HEIGHT)
        map_x = map_value(normalised_coordinates[0], 0, (self.visibility_radius * 2 + 1) * C_WIDTH, 0, self.size[0]) + self.rect.left
        map_y = map_value(normalised_coordinates[1], 0, (self.visibility_radius * 2 + 1) * C_HEIGHT, 0, self.size[1]) + self.rect.top

        return (map_x, map_y)