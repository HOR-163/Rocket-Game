import pygame
from math import *

from CONSTANTS import *
from bezier import *
from coordinate_systems import *

def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

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
    def __init__(self, x_pos, y_pos, acceleration, boost, max_speed, fuel, collision_points, image):

        # Rocket's position TODO: convert position to tuple[int, int]
        self.x_pos = x_pos
        self.y_pos = y_pos

        # Accelerattion
        self.acceleration = acceleration
        self.boost = boost

        # Speed and angle variables TODO: make speed a vector aka tuple[float, float]
        self.max_speed = max_speed
        self.angle = 0
        self.x_speed = 0
        self.y_speed = 0

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

        self.debug = True




    def draw(self, screen, scale: float, color):
        # Put the image in the center of our imaginary "position point" aka when rotating the rocket
        # it rotates from the center, not from the upper left corner of the image (sprite)
        # Also apply scale to the rocket
        x_image_offset = cubic_bezier(0, 0, 50, 0, 50, 100, 100, 100, self.x_speed / self.max_speed) #,screen, position=(WIDTH - 100, HEIGHT - 100))
        y_image_offset = cubic_bezier(0, 0, 50, 0, 50, 100, 100, 100, self.y_speed / self.max_speed) #,screen, color='blue',position=(WIDTH - 100, HEIGHT- 200))
        image_x = WIDTH / 2 - x_image_offset * WIDTH / (2 * 100)
        image_y = HEIGHT / 2 + y_image_offset * HEIGHT / (2 * 100)

        scaled_image = pygame.transform.scale(self.image, (self.image_size[0] * scale, self.image_size[1] * scale))
        scaled_rotated_image = pygame.transform.rotate(scaled_image, self.angle)

        self.rect = scaled_rotated_image.get_rect(center = (image_x, image_y))
        self.mask = pygame.mask.from_surface(scaled_rotated_image)

        if self.debug:
            draw_rect_alpha(screen, color, self.rect)
        screen.blit(scaled_rotated_image, self.rect)


        return (image_x, image_y)

    def update(self, screen, dt, scale, keys, color):
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
            self.reset()

        # Limit the speeds to be in range of maximum speed
        air_speed = sqrt(self.x_speed ** 2 + self.y_speed ** 2)
        if air_speed > self.max_speed:
            self.x_speed = self.max_speed / air_speed * self.x_speed
            self.y_speed = self.max_speed / air_speed * self.y_speed
        
        self.x_pos -= self.x_speed * dt
        self.y_pos += self.y_speed * dt

        # print(x_offset_amount, y_offset_amount)



        lowest = None
        for index, point in enumerate(self.collision_points):
            point_y_position = point.screen_position[1]
            if lowest is None or lowest.screen_position[1] < point_y_position:
                lowest = point

        # If the lowest point intersects with ground
        if screen_to_world_coordinates((None, lowest.screen_position[1]), self.position, scale)[1] > HEIGHT / 2 + C_HEIGHT / 2:
            if self.debug:
                pygame.draw.circle(screen, "green", lowest.screen_position, 3)
            
            self.y_pos += (world_to_screen_coordinates((None, HEIGHT / 2 + C_HEIGHT / 2 + 1), self.position, scale)[1] - lowest.screen_position[1])
            self.x_speed = self.x_speed - self.x_speed * GROUND_FRICTION
            self.y_speed = 0 

        image_offset = self.draw(screen, scale, color)


        for index, point in enumerate(self.collision_points):
            point.update(self.angle, image_offset[0], image_offset[1], scale)
            if self.debug:
                point.draw(screen, scale, self.image_size, image_offset, COLORS[index % 8], self.angle)

        return air_speed
    
    @property
    def position(self):
        return (self.x_pos, self.y_pos)
    
    def reset(self):
        self.x_pos = WIDTH / 2
        self.y_pos = HEIGHT / 2
        self.x_speed = 0
        self.y_speed = 0
        self.angle = 0
        self.fuel = self.start_fuel

"""#######################################
   GAMEOBJECTS (MONEY, FUEL, OBSTACLES)
#######################################"""

class Object(pygame.sprite.Sprite):
    def __init__(self, object_type: str, level: int | None, position: tuple[int, int], image):
        self.object_type = object_type # fuel, money
        self.level = level # 1,2,3
        self.position = position # world position
        self.chunk_coordinates = world_to_chunk_coordinates(self.position)

        # All variables for drawing the object and collision detection
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        
        self.mask = pygame.mask.from_surface(self.image)

        self.image_size = self.image.get_width(), self.image.get_height()
        self.rect = pygame.Rect(0,1000, self.image_size[0], self.image_size[1]) # move the rect to impossibly low, that the collsiion wouldn't occur on the first frame

        self.scale_overwrite = 2

    def draw(self, screen, scale, rocket_position):
        screen_position = world_to_screen_coordinates(self.position, rocket_position, scale)
        if (screen_position[0] >= 0 - self.image_size[0] * 2 and 
            screen_position[0] <= WIDTH + self.image_size[0] * 2 and 
            screen_position[1] >= 0 - self.image_size[1] * 2 and 
            screen_position[1] <= HEIGHT + self.image_size[1] * 2 and 
            self.chunk_coordinates[1] >= 2):
            
            scaled_image = pygame.transform.scale(self.image, (self.image_size[0] * scale * self.scale_overwrite, self.image_size[1] * scale * self.scale_overwrite))
            self.mask = pygame.mask.from_surface(scaled_image)
            self.rect = scaled_image.get_rect(center = screen_position)
            screen.blit(scaled_image, self.rect)

# List of money, fuel and obstacles (all that need collision detection)
collision_group = pygame.sprite.Group()

# Just used for the first time
last_chunk_coordinates = (0,0)

def create_objects_for_the_first_time(images: dict) -> None:
    global objects

    for object_type in powerup_amounts: # Go through all powerup types
        for _ in range(powerup_amounts[object_type]): # Amount of powerups
            random_coordinates = create_random_coordinates(chunk_to_world_coordinates((-generation_radius, generation_radius)), 
                                                            (C_WIDTH * (generation_radius * 2 + 1), C_HEIGHT * (generation_radius * 2 + 1)))
            if object_type == "money":
                object_level = get_money_level(world_to_chunk_coordinates(random_coordinates))
                collision_group.add(Object(object_type, object_level, random_coordinates, images[object_level]))
            
            elif object_type == "fuel":
                object_level = get_fuel_level(world_to_chunk_coordinates(random_coordinates))
                collision_group.add(Object(object_type, object_level, random_coordinates, images[object_level + 3]))
    
    # Create x amount of obstacles 

    for _ in range(obstacle_amount):
        random_coordinates = create_random_coordinates(chunk_to_world_coordinates((-generation_radius, generation_radius)), 
                                                            (C_WIDTH * (generation_radius * 2 + 1), C_HEIGHT * (generation_radius * 2 + 1)))
        # Get the first level of obstacles, then get a random obstacle type from there
        object_type = obstacle_types[1][random.randint(0, len(obstacle_types[1])) - 1] # len - 1 (lists start from 0)
        collision_group.add(Object(object_type, 1, random_coordinates, images[object_type])) # Instead of 1, there could be None, because that value is unused for obstacles


def reset_objects(images: dict) -> None:
    for object in collision_group:
        object_type = object.object_type
        object_level = object.level
        random_coordinates = create_random_coordinates(chunk_to_world_coordinates((-generation_radius, generation_radius)), 
                                                            (C_WIDTH * (generation_radius * 2 + 1), C_HEIGHT * (generation_radius * 2 + 1)))
        if object_type == "money":
            object_level = get_money_level(world_to_chunk_coordinates(random_coordinates))
            object.__init__(object_type, object_level, random_coordinates, images[object_level])
        
        elif object_type == "fuel":
            object_level = get_fuel_level(world_to_chunk_coordinates(random_coordinates))
            object.__init__(object_type, object_level, random_coordinates, images[object_level + 3])

        elif object_type in all_obstacles:
            # Get the first level of obstacles, then get a random obstacle type from there
            object_type = obstacle_types[1][random.randint(0, len(obstacle_types[1])) - 1] # len - 1 (lists start from 0)
            object.__init__(object_type, 1, random_coordinates, images[object_type]) # Instead of 1, there could be None, because that value is unused for obstacles


            
def update_objects(chunk_coordinates: tuple[int, int], images) -> None:
    global last_chunk_coordinates

    if last_chunk_coordinates != chunk_coordinates:

        # See if some powerups could be removed
        for object in collision_group:
            if object.chunk_coordinates[1] < chunk_coordinates[1] - generation_radius: # object is too low
                create_new_object(object, chunk_coordinates, "up", images)
            elif object.chunk_coordinates[1] > chunk_coordinates[1] + generation_radius: # object is too high
                create_new_object(object, chunk_coordinates, "down", images)
            elif object.chunk_coordinates[0] < chunk_coordinates[0] - generation_radius: # object is too left
                create_new_object(object, chunk_coordinates, "right", images)
            elif object.chunk_coordinates[0] > chunk_coordinates[0] + generation_radius: # object is too right
                create_new_object(object, chunk_coordinates, "left", images)
        last_chunk_coordinates = chunk_coordinates

def get_money_level(chunk_coordinates: tuple[int,int]) -> int:
    # Create the odds of each powerup to be created
    if chunk_coordinates[1] + 1 < 100:
        coin_percent = 100 - 100 * (chunk_coordinates[1] + 2) / 400
        cash_percent = 100 - coin_percent
        #money_bag_percent = 0
    elif chunk_coordinates[1] + 1 >= 100 and chunk_coordinates[1] + 1 <= 199:
        coin_percent = 50 - 50 * (chunk_coordinates[1] - 100 + 2) / 250
        cash_percent = 50 + 50 * (chunk_coordinates[1] - 100 + 2) / 500
        #money_bag_percent = 100 - coin_percent - cash_percent
    elif chunk_coordinates[1] + 1 >= 200:
        coin_percent = 20
        cash_percent = 60
        #money_bag_percent = 20

    # Create a random number to find the level of fuel
    rng = random.randint(0,100)

    if rng < coin_percent:
        # make a coin
        return 1
    elif rng >= coin_percent and rng < coin_percent + cash_percent:
        # make a cash
        return 2
    # make a money_bag
    return 3

def get_fuel_level(chunk_coordinates: tuple[int,int]) -> int:
    # Create the odds of each powerup to be created
    if chunk_coordinates[1] + 1 < 100:
        small_percent = 100 - 100 * (chunk_coordinates[1] + 2) / 400
        medium_percent = 100 - small_percent
        #large_percent = 0
    elif chunk_coordinates[1] + 1 >= 100 and chunk_coordinates[1] + 1 <= 199:
        small_percent = 50 - 50 * (chunk_coordinates[1] - 100 + 2) / 250
        medium_percent = 50 + 50 * (chunk_coordinates[1] - 100 + 2) / 500
        #large_percent = 100 - small_percent - medium_percent
    elif chunk_coordinates[1] + 1 >= 200:
        small_percent = 20
        medium_percent = 60
        #large_percent = 20

    # Create a random number to find the level of fuel
    rng = random.randint(0,100)
        
    if rng < small_percent:
        # make a coin
        return 1
    elif rng >= small_percent and rng < small_percent + medium_percent:
        # make a cash
        return 2
    # make a money_bag
    return 3

def get_obstacle_level(chunk_coordinates: tuple[int, int]) -> int:
    if chunk_coordinates[1] < 100:
        return 1
    elif chunk_coordinates[1] < 200:
        return 2
    elif chunk_coordinates[1] >= 200:
        return 3

def create_new_object(object, chunk_coordinates: tuple[int, int], direction: str, images: dict) -> None:
    object_type = object.object_type

    # Create random coordinates, where the powerup is going to be placed
    if direction == "up":
        random_position = create_random_coordinates(chunk_to_world_coordinates((chunk_coordinates[0] - generation_radius,         # start_x
                                                                            chunk_coordinates[1] + generation_radius - 1)),       # start_y
                                                                            (C_WIDTH * (generation_radius * 2 + 1), C_HEIGHT))   # size
    elif direction == "down":
        random_position = create_random_coordinates(chunk_to_world_coordinates((chunk_coordinates[0] - generation_radius,         # start_x
                                                                            chunk_coordinates[1] - generation_radius - 1)),       # start_y
                                                                            (C_WIDTH * (generation_radius * 2 + 1), C_HEIGHT))    # size
    elif direction == "right":
        random_position = create_random_coordinates(chunk_to_world_coordinates((chunk_coordinates[0] + generation_radius - 1,     # start_x
                                                                            chunk_coordinates[1] + generation_radius)),           # start_y
                                                                            (C_WIDTH, C_HEIGHT * (generation_radius * 2 + 1)))    # size
    elif direction == "left":
        random_position = create_random_coordinates(chunk_to_world_coordinates((chunk_coordinates[0] - generation_radius - 1,     # start_x
                                                                            chunk_coordinates[1] + generation_radius)),           # start_y
                                                                            (C_WIDTH, C_HEIGHT * (generation_radius * 2 + 1)))    # size

    # Create powerups according to their type
    if object_type == "money":
        object_level = get_money_level(chunk_coordinates)
        object.__init__(object_type, object_level, random_position, images[object_level])

    elif object_type == "fuel":
        object_level = get_fuel_level(chunk_coordinates)
        object.__init__(object_type, object_level, random_position, images[object_level + 3])
    elif object_type in all_obstacles:
        obstacle_level = get_obstacle_level(chunk_coordinates)
        obstacle_type = obstacle_types[obstacle_level][random.randint(0, len(obstacle_types[obstacle_level]) - 1)]
        object.__init__(obstacle_type, obstacle_level, random_position, images[obstacle_type])


class Player():
    def __init__(self, starting_money = 100) :
        self.starting_money = starting_money
        self.money = starting_money